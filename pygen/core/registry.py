"""Registry: memuat seluruh bank data template (*.json) dari folder templates/
dan memvalidasi strukturnya.

Mendukung struktur sub-folder untuk organisasi domain:
  templates/
  ├── prompt_eng/
  │   ├── api_connection.json
  │   └── ...
  ├── data/
  │   ├── csv_tools.json
  │   └── ...
  └── ...

Setiap sub-folder = satu domain. Folder templates/ datar (tanpa sub-folder)
juga tetap didukung untuk backward compatibility.

Mode lazy: hanya load domain yang diminta user, bukan semuanya sekaligus.
"""

import json
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")

REQUIRED_TEMPLATE_KEYS = {"id", "title", "description", "imports", "fields", "code", "sample_values"}
REQUIRED_FIELD_KEYS = {"name", "label", "type", "default"}
VALID_FIELD_TYPES = {"identifier", "text", "list", "int", "choice", "bool", "multi_line", "args", "optional"}


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


def _load_categories_from_dir(categories_dir: str, domain_name: str = None) -> list:
    """Muat semua file *.json dari satu direktori (bisa root templates/ atau sub-folder).
    Setiap kategori: {"category": str, "label": str, "domain": str, "templates": [ ... ]}
    """
    if not os.path.isdir(categories_dir):
        raise TemplateBankError(f"Folder bank data template tidak ditemukan: {categories_dir}")

    categories = []
    for filename in sorted(os.listdir(categories_dir)):
        if not filename.endswith(".json"):
            continue
        if filename.startswith("_"):  # skip _meta.json, _internal, etc.
            continue
        full_path = os.path.join(categories_dir, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise TemplateBankError(f"File bank data rusak (bukan JSON valid): {filename} — {e}")

        for required_key in ("category", "label", "templates"):
            if required_key not in data:
                raise TemplateBankError(f"File {full_path} kehilangan key wajib '{required_key}'")

        for tpl in data["templates"]:
            _validate_template(tpl, full_path)

        # Inject domain name into each template for provenance tracking
        if domain_name:
            data["domain"] = domain_name
            for tpl in data["templates"]:
                tpl["_domain"] = domain_name

        categories.append(data)

    if not categories:
        raise TemplateBankError(f"Tidak ada file bank data template (*.json) ditemukan di {categories_dir}")

    return categories


def _detect_structure(templates_dir: str = TEMPLATES_DIR) -> tuple:
    """Deteksi apakah templates/ menggunakan sub-folder (domain-based) atau flat.
    Returns: (mode, domains_dict) where mode is "flat" or "nested"
    and domains_dict is {"domain_label": "path"} for nested mode.
    """
    if not os.path.isdir(templates_dir):
        return "flat", {}

    entries = os.listdir(templates_dir)
    has_subdirs = any(
        os.path.isdir(os.path.join(templates_dir, e)) and not e.startswith(".")
        for e in entries
    )

    if has_subdirs:
        domains = {}
        for entry in sorted(os.listdir(templates_dir)):
            full = os.path.join(templates_dir, entry)
            if os.path.isdir(full) and not entry.startswith("."):
                # Check if sub-folder contains .json files
                if any(f.endswith(".json") for f in os.listdir(full)):
                    domains[entry] = full
        return "nested", domains
    else:
        return "flat", {}


def get_domains(templates_dir: str = TEMPLATES_DIR) -> list:
    """Dapatkan daftar domain yang tersedia. Untuk mode nested, baca file
    _meta.json di setiap sub-folder (atau fallback ke nama folder).
    Returns list of {"key": "folder_name", "label": "Display Label"}.
    """
    mode, paths = _detect_structure(templates_dir)
    if mode == "flat":
        return [{"key": "__root__", "label": "Umum"}]
    
    domains = []
    for key, path in sorted(paths.items()):
        meta_file = os.path.join(path, "_meta.json")
        if os.path.isfile(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                domains.append({"key": key, "label": meta.get("label", key)})
            except json.JSONDecodeError:
                domains.append({"key": key, "label": key})
        else:
            # Fallback: prettify folder name
            label = key.replace("_", " ").title()
            domains.append({"key": key, "label": label})
    return domains


def load_categories(templates_dir: str = TEMPLATES_DIR, domain: str = None) -> list:
    """Muat semua template dari folder templates/.
    
    Jika domain=None: load semua domain (untuk backward compat).
    Jika domain="prompt_eng": hanya load dari templates/prompt_eng/.
    Jika struktur flat: abaikan parameter domain.
    """
    mode, domain_paths = _detect_structure(templates_dir)

    if mode == "nested":
        if domain and domain in domain_paths:
            return _load_categories_from_dir(domain_paths[domain], domain_name=domain)
        elif domain is None:
            # Load all domains
            all_categories = []
            for domain_key, domain_path in sorted(domain_paths.items()):
                all_categories.extend(
                    _load_categories_from_dir(domain_path, domain_name=domain_key)
                )
            if not all_categories:
                raise TemplateBankError(
                    f"Tidak ada file bank data template ditemukan di {templates_dir}"
                )
            return all_categories
        else:
            available = list(domain_paths.keys())
            raise TemplateBankError(
                f"Domain '{domain}' tidak ditemukan. Tersedia: {available}"
            )

    # Flat mode (legacy)
    return _load_categories_from_dir(templates_dir)


def find_template(template_id: str, categories: list = None) -> dict:
    """Cari template berdasarkan id di seluruh kategori. Kembalikan None jika tidak ada."""
    categories = categories if categories is not None else load_categories()
    for cat in categories:
        for tpl in cat["templates"]:
            if tpl["id"] == template_id:
                return tpl
    return None


def search_templates(query: str, categories: list = None) -> list:
    """Cari template berdasarkan kata kunci (di id, title, description).
    Case-insensitive. Kembalikan list template yang cocok.
    """
    categories = categories if categories is not None else load_categories()
    query_lower = query.lower()
    results = []
    for cat in categories:
        for tpl in cat["templates"]:
            searchable = f"{tpl['id']} {tpl['title']} {tpl.get('description', '')}".lower()
            if query_lower in searchable:
                results.append(tpl)
    return results


def list_all_template_ids(categories: list = None) -> list:
    """List semua template id yang tersedia."""
    categories = categories if categories is not None else load_categories()
    ids = []
    for cat in categories:
        for tpl in cat["templates"]:
            ids.append(tpl["id"])
    return sorted(ids)
