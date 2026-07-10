"""Test suite: memastikan SETIAP template di bank data (templates/*.json)
berhasil di-render dengan sample_values-nya dan hasilnya valid secara
sintaks Python. Template yang gagal test ini tidak boleh dirilis.

Jalankan: python -m pytest tests/ -v
atau tanpa pytest: python tests/test_templates.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pygen.core.registry import load_categories
from pygen.core.template_engine import render
from pygen.core.validator import validate_syntax
from pygen.core.compositor import compose, GeneratedUnit


class TestTemplateBank(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.categories = load_categories()

    def test_bank_not_empty(self):
        self.assertGreater(len(self.categories), 0, "Bank data template kosong")
        total_templates = sum(len(c["templates"]) for c in self.categories)
        self.assertGreater(total_templates, 0, "Tidak ada template sama sekali")

    def test_all_ids_unique(self):
        ids = []
        for cat in self.categories:
            for tpl in cat["templates"]:
                ids.append(tpl["id"])
        duplicates = {i for i in ids if ids.count(i) > 1}
        self.assertEqual(duplicates, set(), f"Ada id template duplikat: {duplicates}")

    def test_every_template_renders_and_parses(self):
        failures = []
        for cat in self.categories:
            for tpl in cat["templates"]:
                with self.subTest(template=tpl["id"]):
                    try:
                        code = render(tpl, tpl["sample_values"])
                        validate_syntax(code, context_label=tpl["id"])
                    except Exception as e:
                        failures.append(f"{tpl['id']}: {e}")
        self.assertEqual(failures, [], "Template gagal render/validasi:\n" + "\n".join(failures))

    def test_no_leftover_placeholders(self):
        """Pastikan tidak ada {{...}} tersisa setelah render dengan sample_values."""
        for cat in self.categories:
            for tpl in cat["templates"]:
                with self.subTest(template=tpl["id"]):
                    code = render(tpl, tpl["sample_values"])
                    self.assertNotIn("{{", code, f"Placeholder tersisa di template {tpl['id']}")

    def test_compositor_combines_all_templates_together(self):
        """Uji berat: rangkai SEMUA template bank jadi satu file, harus tetap valid."""
        units = []
        for cat in self.categories:
            for tpl in cat["templates"]:
                code = render(tpl, tpl["sample_values"])
                units.append(GeneratedUnit(tpl["id"], tpl["title"], tpl["imports"], code))
        final_code = compose(units)
        validate_syntax(final_code, context_label="composite semua template")
        self.assertIn("import", final_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
