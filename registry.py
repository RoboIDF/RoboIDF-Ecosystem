"""Explicit offline CSV registry. No dynamic imports and no hardware execution."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
from adapter import read_csv, write_csv
from roboidf import Dataset, MockRobot
from roboidf.validation import VERSION, digest, example_contract, hardware_precheck, report, source_check, validate_contract

REGISTRY_VERSION = 'registry.v1'


def example_manifest():
    fixture = MockRobot().collect(seed=91, split='validation', samples=8)
    return {'schema_version': REGISTRY_VERSION, 'id': 'synthetic-csv', 'implementation': 'builtin-csv-v1',
            'level': 'offline-synthetic', 'source': example_contract()['source'], 'contract': example_contract(),
            'evidence': {'kind': 'synthetic-csv-roundtrip', 'seed': 91, 'samples': 8, 'dataset_sha256': fixture.digest()}}


class Registry:
    def __init__(self):
        self._manifests = {}

    def register(self, manifest):
        allowed = {'schema_version', 'id', 'implementation', 'level', 'source', 'contract', 'evidence'}
        if not isinstance(manifest, dict) or set(manifest) != allowed:
            raise ValueError('manifest must contain only the documented fields; executable entrypoints prohibited')
        if manifest.get('schema_version') != REGISTRY_VERSION:
            raise ValueError('unsupported registry schema_version')
        ident = manifest.get('id')
        if not isinstance(ident, str) or not ident.strip() or ident in self._manifests:
            raise ValueError('nonempty unique registry id required')
        if manifest.get('implementation') != 'builtin-csv-v1':
            raise ValueError('only explicitly bound builtin-csv-v1 is supported')
        if manifest.get('level') != 'offline-synthetic':
            raise ValueError('only offline-synthetic evidence level supported')
        source_check(manifest.get('source'))
        contract = manifest.get('contract')
        validate_contract(contract)
        if contract['mode'] != 'offline' or contract['adapter']['kind'] != 'offline-csv':
            raise ValueError('hardware plugins are pending and cannot register')
        joints = contract['joints']
        if len(joints) != 1 or joints[0]['type'] != 'prismatic':
            raise ValueError('builtin CSV supports one scalar prismatic joint only')
        evidence = manifest.get('evidence')
        expected = example_manifest()['evidence']
        if evidence != expected:
            raise ValueError('required reproducible synthetic fixture evidence is missing or incompatible')
        # Exercise the actual bound implementation, not code named by a manifest.
        fixture = MockRobot().collect(seed=91, split='validation', samples=8)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fixture.csv'
            write_csv(fixture, path)
            observed = read_csv(path, split='validation', seed=91)
        if not isinstance(observed, Dataset) or observed.digest() != evidence['dataset_sha256']:
            raise ValueError('actual CSV roundtrip evidence failed')
        self._manifests[ident] = copy.deepcopy(manifest)
        return report(passed=True, registry_version=REGISTRY_VERSION, scope='offline-synthetic',
                      plugin_id=ident, manifest_sha256=digest(manifest), evidence=copy.deepcopy(evidence))

    def read(self, ident, path, *, split, seed):
        if ident not in self._manifests:
            raise ValueError('plugin not registered')
        return read_csv(path, split=split, seed=seed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--hardware', action='store_true')
    parser.add_argument('--output', type=Path, default=Path('artifacts/registry.json'))
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text()) if args.manifest else example_manifest()
        if args.hardware:
            result = hardware_precheck(manifest.get('contract', {}))
        else:
            result = Registry().register(manifest)
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        result = report(passed=False, reason=str(exc))
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n')
    except OSError as exc:
        result = report(passed=False, reason='cannot save report: ' + str(exc))
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
