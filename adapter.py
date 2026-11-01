"""Example offline CSV adapter; never connects to or commands hardware."""
import csv
import json
import math
from dataclasses import asdict
from pathlib import Path
from roboidf import Dataset, MockRobot, fit, rollout_rmse

FIELDS=['time_s','velocity_m_s','effort_n']

def read_csv(path,*,split,seed):
    with Path(path).open(newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('expected columns: '+','.join(FIELDS))
        rows=list(reader)
    if len(rows)<4 or any(set(r)!=set(FIELDS) or any(v is None for v in r.values()) for r in rows):
        raise ValueError('need >=4 complete rows')
    if rows[-1]['effort_n']!='':
        raise ValueError('terminal effort must be empty (no terminal transition)')
    times=[float(r['time_s']) for r in rows]
    if not all(math.isfinite(t) for t in times):
        raise ValueError('finite timestamps required')
    dt=times[1]-times[0]
    if dt<=0 or any(not math.isclose(b-a,dt,rel_tol=1e-8,abs_tol=1e-12) for a,b in zip(times,times[1:])):
        raise ValueError('strictly increasing uniformly sampled timestamps required')
    return Dataset(dt,tuple(float(r['velocity_m_s']) for r in rows),
                   tuple(float(r['effort_n']) for r in rows[:-1]),split,seed)

def write_csv(data,path):
    with Path(path).open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(FIELDS)
        for i,v in enumerate(data.velocity):
            writer.writerow([i*data.dt,v,data.effort[i] if i<len(data.effort) else ''])

def demo(output=Path('artifacts')):
    output.mkdir(parents=True,exist_ok=True)
    robot=MockRobot()
    for split,seed in [('train',17),('validation',18)]:
        write_csv(robot.collect(seed=seed,split=split),output/f'{split}.csv')
    train=read_csv(output/'train.csv',split='train',seed=17)
    validation=read_csv(output/'validation.csv',split='validation',seed=18)
    model=fit(train);error=rollout_rmse(model,validation)
    result={'schema_version':'m0.v1','adapter':'example-csv-v1','scope':'synthetic-offline-only',
            'train_sha256':train.digest(),'validation_sha256':validation.digest(),
            'model':asdict(model),'rollout_rmse_m_s':error,'passed':error<1e-8}
    (output/'adapter.json').write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    return result

if __name__=='__main__':
    result=demo();print(json.dumps(result,sort_keys=True))
    raise SystemExit(0 if result['passed'] else 1)
