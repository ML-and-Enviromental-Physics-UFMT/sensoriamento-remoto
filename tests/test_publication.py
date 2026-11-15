import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicationTests(unittest.TestCase):
    def test_public_files_have_no_legacy_binaries_or_notebook_outputs(self):
        _, failures = load_script('auditar_publicacao').audit()
        self.assertEqual(failures, [])

    def test_sample_matches_generator_and_has_no_geographic_crs(self):
        import numpy as np
        import rasterio

        generator = load_script('gerar_dados_sinteticos')
        with rasterio.open(generator.OUTPUT) as dataset:
            np.testing.assert_array_equal(dataset.read(), generator.generate())
            self.assertEqual(dataset.count, 9)
            self.assertIsNone(dataset.crs)
            self.assertEqual(dataset.tags()['LICENSE'], 'CC-BY-4.0')
            self.assertIn('Synthetic', dataset.tags()['SOURCE'])
