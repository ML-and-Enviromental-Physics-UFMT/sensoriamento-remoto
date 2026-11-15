"""Verificações dos caminhos compartilhados após a migração por assunto."""
import ast
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryStructureTests(unittest.TestCase):
    def test_learning_links_resolve(self):
        documents = [ROOT / 'README.md', ROOT / 'trilha-de-aprendizagem.md', ROOT / 'CONTRIBUTING.md']
        for folder in ['conteudo', 'projetos', 'referencias']:
            documents.extend((ROOT / folder).rglob('*.md'))
        for path in documents:
            for link in re.findall(r'\]\((<[^>]+>|[^)]+)\)', path.read_text()):
                link = link.strip('<>')
                if '://' in link or link.startswith(('#', 'mailto:')):
                    continue
                with self.subTest(file=path.relative_to(ROOT), link=link):
                    self.assertTrue((path.parent / link.split('#')[0]).exists())

    def test_exercises_find_the_shared_raster(self):
        for path in (ROOT / 'conteudo').rglob('exercicios/*.py'):
            scope = {'Path': Path, '__file__': str(path)}
            tree = ast.parse(path.read_text())
            for statement in ast.walk(tree):
                if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
                    continue
                target = statement.targets[0]
                if not isinstance(target, ast.Name):
                    continue
                name = target.id
                if name not in {'REPO', 'repo', '_HERE', '_DEFAULT', 'EXEMPLO', 'default_tif'}:
                    continue
                value = eval(compile(ast.Expression(statement.value), str(path), 'eval'), scope)
                scope[name] = value
                if name in {'REPO', 'repo'}:
                    with self.subTest(file=path.relative_to(ROOT), variable=name):
                        self.assertEqual(value, ROOT)
                if name in {'_DEFAULT', 'EXEMPLO', 'default_tif'}:
                    with self.subTest(file=path.relative_to(ROOT), variable=name):
                        self.assertEqual(value, ROOT / 'data/exemplos/exemplo_sintetico.tif')
                        self.assertTrue(value.is_file())

    def test_notebook_locations_from_root_and_notebook_directory(self):
        paths = [*(ROOT / 'conteudo').rglob('*.ipynb'), *(ROOT / 'projetos').rglob('*.ipynb')]
        previous = Path.cwd()
        try:
            for path in paths:
                notebook = json.loads(path.read_text())
                for cwd in [ROOT, path.parent]:
                    os.chdir(cwd)
                    scope = {'Path': Path}
                    for cell in notebook['cells']:
                        if cell['cell_type'] != 'code':
                            continue
                        source = ''.join(cell['source'])
                        if source.startswith(('%', '!')):
                            continue
                        for statement in ast.parse(source).body:
                            if not isinstance(statement, ast.Assign):
                                continue
                            if len(statement.targets) != 1 or not isinstance(statement.targets[0], ast.Name):
                                continue
                            name = statement.targets[0].id
                            if name not in {'REPO', 'PROJETO', 'EXEMPLO', 'DATA', 'RASTER_PATH', 'OUT'}:
                                continue
                            value = eval(compile(ast.Expression(statement.value), str(path), 'eval'), scope)
                            scope[name] = value
                            with self.subTest(file=path.relative_to(ROOT), cwd=cwd, variable=name):
                                if name == 'REPO':
                                    self.assertEqual(value, ROOT)
                                elif name in {'EXEMPLO', 'DATA', 'RASTER_PATH'}:
                                    self.assertEqual(value, ROOT / 'data/exemplos/exemplo_sintetico.tif')
                                elif name == 'OUT':
                                    self.assertEqual(value, path.parent.parent / 'figuras')
        finally:
            os.chdir(previous)

    def test_migration_targets_exist(self):
        mapping = json.loads((ROOT / 'docs/decisoes/mapa-de-migracao.json').read_text())
        for old, new in mapping.items():
            with self.subTest(old=old):
                self.assertTrue((ROOT / new).exists())


if __name__ == '__main__':
    unittest.main()
