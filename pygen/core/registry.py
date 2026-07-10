"""Registry: memuat seluruh bank data template (*.json) dari folder templates/
dan memvalidasi strukturnya. Ini satu-satunya tempat yang tahu di mana file
bank data berada — kode lain cukup panggil load_categories().
"""

import json
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")

REQUIRED_TEMPLATE_KEYS = {"id", "title", "description", "imports", "fields", "code", "sample_values"}
REQUIRED_FIELD_KEYS = {"name", "label", "type", "default"}
VALID_FIELD_TYPES = {"identifier", "text", "list", "int", "choice"}


class TemplateBankError(Exception):
    """Dilempar jika ada file bank data yang rusak atau tidak sesuai skema."""


def _validate_template(tpl: dict, source_file: str):
    missing = REQUIRED_TEMPLATE_KEYS - tpl.keys()
    if missing:
        raise TemplateBankError(
            f"Template di {source_file} kehilangan key wajib: {missing} (id={tpl.get('id')})"
        )
    for field in tpl["fields"]:
        f_missing = REQUIRED_FIELD_KEYS - field.keys()
        if f_missing:
            raise TemplateBankError(
                f"Field pada template '{tpl['id']}' di {source_file} kehilangan key: {f_missing}"
            )
        if field["type"] not in VALID_FIELD_TYPES:
            raise TemplateBankError(
                f"Field '{field['name']}' pada template '{tpl['id']}' punya type tidak dikenal: {field['type']}"
            )
        if field["name"] not in tpl["sample_values"]:
            raise TemplateBankError(
                f"Field '{field['name']}' pada template '{tpl['id']}' tidak punya sample_values "
                f"(wajib untuk test otomatis)"
            )


def load_categories(templates_dir: str = TEMPLATES_DIR) -> list:
    """Muat semua file *.json di templates_dir, validasi, kembalikan list kategori.

    Setiap kategori: {"category": str, "label": str, "templates": [ ... ]}
    """
    if not os.path.isdir(templates_dir):
        raise TemplateBankError(f"Folder bank data template tidak ditemukan: {templates_dir}")

    categories = []
    for filename in sorted(os.listdir(templates_dir)):
        if not filename.endswith(".json"):
            continue
        full_path = os.path.join(templates_dir, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise TemplateBankError(f"File bank data rusak (bukan JSON valid): {filename} — {e}")

        for required_key in ("category", "label", "templates"):
            if required_key not in data:
                raise TemplateBankError(f"File {filename} kehilangan key wajib '{required_key}'")

        for tpl in data["templates"]:
            _validate_template(tpl, filename)

        categories.append(data)

    if not categories:
        raise TemplateBankError(f"Tidak ada file bank data template ditemukan di {templates_dir}")

    return categories


def find_template(template_id: str, categories: list = None) -> dict:
    """Cari template berdasarkan id di seluruh kategori. Kembalikan None jika tidak ada."""
    categories = categories if categories is not None else load_categories()
    for cat in categories:
        for tpl in cat["templates"]:
            if tpl["id"] == template_id:
                return tpl
    return None
