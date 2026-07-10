"""Test suite: memastikan SETIAP template di bank data (templates/*.json)
berhasil di-render dengan sample_values-nya dan hasilnya valid secara
sintaks Python. Template yang gagal test ini tidak boleh dirilis.

Jalankan: python -m pytest tests/ -v
atau tanpa pytest: python tests/test_templates.py
"""

import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pygen.core.registry import load_categories
from pygen.core.template_engine import render
from pygen.core.validator import validate_syntax
from pygen.core.compositor import compose, GeneratedUnit

PLACEHOLDER_REMNANT = re.compile(r"\{\{(\w+)\}\}")


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
        self.assertEqual(duplicates, set(), "Ada id template duplikat: " + str(duplicates))

    def test_every_template_renders_and_parses(self):
        failures = []
        for cat in self.categories:
            for tpl in cat["templates"]:
                with self.subTest(template=tpl["id"]):
                    try:
                        code = render(tpl, tpl["sample_values"])
                        validate_syntax(code, context_label=tpl["id"])
                    except Exception as e:
                        failures.append(tpl["id"] + ": " + str(e))
        self.assertEqual(failures, [], "Template gagal render/validasi:\n" + "\n".join(failures))

    def test_no_leftover_placeholders(self):
        """Pastikan tidak ada {{namafield}} tersisa setelah render.
        {{ literal di kode Python (seperti f-string escape) tidak dihitung gagal.
        """
        for cat in self.categories:
            for tpl in cat["templates"]:
                with self.subTest(template=tpl["id"]):
                    code = render(tpl, tpl["sample_values"])
                    match = PLACEHOLDER_REMNANT.search(code)
                    if match:
                        field_name = match.group(1)
                        self.fail(
                            "Placeholder {{" + field_name + "}} tersisa di template " + tpl["id"]
                        )

    def test_compositor_combines_all_templates_together(self):
        """Uji berat: rangkai SEMUA template bank jadi satu file, harus tetap valid."""
        units = []
        for cat in self.categories:
            for tpl in cat["templates"]:
                code = render(tpl, tpl["sample_values"])
                units.append(
                    GeneratedUnit(
                        template_id=tpl["id"],
                        title=tpl["title"],
                        imports=tpl.get("imports", []),
                        code=code,
                        requires=tpl.get("requires", {}),
                    )
                )
        final_code = compose(units)
        validate_syntax(final_code, context_label="composite semua template")
        self.assertIn("import", final_code)


class TestRegistry(unittest.TestCase):

    def test_domains_available(self):
        from pygen.core.registry import get_domains
        domains = get_domains()
        self.assertGreater(len(domains), 1, "Harus ada lebih dari 1 domain dengan struktur baru")

    def test_lazy_load_per_domain(self):
        from pygen.core.registry import load_categories
        prompt_eng = load_categories(domain="prompt_eng")
        data = load_categories(domain="data")
        all_cats = load_categories()
        total_domain = len(prompt_eng) + len(data)
        self.assertLessEqual(total_domain, len(all_cats),
                             "Total domain partial harus <= total semua domain")

    def test_search(self):
        from pygen.core.registry import search_templates
        results = search_templates("csv")
        self.assertGreater(len(results), 0, "Harus ada template dengan keyword 'csv'")


class TestFullWorkflow(unittest.TestCase):

    def test_cli_entry_importable(self):
        from pygen.cli_entry import main
        self.assertTrue(callable(main))

    def test_batch_workflow_no_crash(self):
        """Simulasi workflow batch: render multi-template, compose, syntax ok."""
        from pygen.core.registry import load_categories, find_template
        categories = load_categories()
        ids = ["csv_reader", "write_json_file", "run_command"]
        units = []
        for tid in ids:
            tpl = find_template(tid, categories)
            if tpl is None:
                continue
            code = render(tpl, tpl["sample_values"])
            validate_syntax(code, context_label=tid)
            units.append(GeneratedUnit(
                template_id=tid,
                title=tpl["title"],
                imports=tpl.get("imports", []),
                code=code,
                requires=tpl.get("requires", {}),
            ))
        self.assertGreater(len(units), 0, "Harus minimal 1 unit berhasil")
        final = compose(units)
        self.assertIn("read_csv", final)
        self.assertIn("write_json", final)
        self.assertIn("run_cmd", final)


if __name__ == "__main__":
    unittest.main(verbosity=2)
