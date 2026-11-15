#!/usr/bin/env python3
"""Confere os arquivos que o Git incluiria na cópia pública, sem alterá-los."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = 'data/exemplos/exemplo_sintetico.tif'


def audit():
    result = subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=ROOT, check=True, capture_output=True,
    )
    failures = []
    paths = sorted(set(result.stdout.decode().strip('\0').split('\0')) - {''})
    for name in paths:
        path = ROOT / name
        if path.is_symlink():
            failures.append(f'{name}: link simbólico exige revisão')
            continue
        if path.suffix.lower() in {'.pdf', '.tif', '.tiff', '.png', '.jpg', '.jpeg'} and name != SYNTHETIC:
            failures.append(f'{name}: material binário sem liberação nesta cópia')
        if name.startswith('legado/canty/') and path.suffix in {'.py', '.sh'}:
            failures.append(f'{name}: código legado externo')
        if path.suffix == '.ipynb':
            notebook = json.loads(path.read_text())
            for cell in notebook['cells']:
                if cell.get('outputs') or cell.get('execution_count') is not None or cell.get('attachments'):
                    failures.append(f'{name}: saídas ou anexos embutidos')
                    break
    return paths, failures


if __name__ == '__main__':
    paths, failures = audit()
    for failure in failures:
        print(failure)
    print(f'{len(paths)} arquivos conferidos; {len(failures)} impedimentos.')
    raise SystemExit(bool(failures))
