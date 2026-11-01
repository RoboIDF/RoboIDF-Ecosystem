import copy
from pathlib import Path
import tempfile
import unittest
from registry import Registry, example_manifest
from adapter import write_csv
from roboidf import MockRobot, Dataset

class RegistryTests(unittest.TestCase):
    def test_explicit_registry_and_actual_csv(self):
        registry=Registry(); manifest=example_manifest()
        registry.register(manifest)
        manifest['contract']['id']='modified'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'fixture.csv'
            original=MockRobot().collect(seed=91,split='validation',samples=8)
            write_csv(original,path)
            data=registry.read('synthetic-csv',path,split='validation',seed=91)
            self.assertIsInstance(data,Dataset)
            self.assertEqual(data.digest(),original.digest())
        with self.assertRaises(ValueError): registry.register(example_manifest())

    def test_bad_manifests_and_escalation(self):
        for key,value in [('schema_version','future'),('level','hardware-validated'),('source',{}),('implementation','os:system'),('evidence',{}),('entrypoint','evil.py')]:
            m=example_manifest(); m[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): Registry().register(m)
        m=example_manifest(); m['contract']['joints'][0]['type']='revolute'
        with self.assertRaises(ValueError): Registry().register(m)
        m=example_manifest(); m['contract']['mode']='hardware'
        with self.assertRaises(ValueError): Registry().register(m)
        with self.assertRaises(ValueError): Registry().read('unknown','none',split='test',seed=1)

    def test_saved_evidence_and_cli(self):
        import json
        import subprocess
        import sys
        from roboidf.validation import compare_replay, hardware_precheck, validate_asset
        root=Path(__file__).resolve().parents[1]
        fixtures=root/'examples'
        load=lambda name: json.loads((fixtures/name).read_text())
        manifest=load('registry-offline-v1.json')
        registry=Registry()
        report=registry.register(manifest)
        self.assertEqual(report,load('registry-evidence-v1.json'))
        data=registry.read(manifest['id'],fixtures/'registry-synthetic-v1.csv',split='validation',seed=91)
        self.assertEqual(data.digest(),manifest['evidence']['dataset_sha256'])
        self.assertEqual(compare_replay(load('replay-reference-v1.json'),load('replay-candidate-v1.json'),rmse_limit=.01),load('replay-error-evidence-v1.json'))
        self.assertEqual(hardware_precheck(load('hardware-pending-v1.json')),load('hardware-refusal-v1.json'))
        assets=load('asset-structure-evidence-v1.json')
        for kind,filename in [('mjcf','synthetic-structure-v1.xml'),('usd','synthetic-header-v1.usda')]:
            self.assertEqual(validate_asset((fixtures/filename).read_text(),kind,manifest['source']),assets[kind])
        for args,code in [([],0),(['--hardware'],1)]:
            p=subprocess.run([sys.executable,str(root/'registry.py'),*args],capture_output=True,text=True,cwd=root)
            self.assertEqual(p.returncode,code,p.stderr)
            self.assertFalse(json.loads(p.stdout)['execution_authorized'])

    def test_cli_saves_report(self):
        import json
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'registry.json'
            p=subprocess.run([sys.executable,'registry.py','--hardware','--output',str(output)],capture_output=True,text=True)
            self.assertEqual(p.returncode,1,p.stderr)
            self.assertEqual(json.loads(output.read_text()),json.loads(p.stdout))
