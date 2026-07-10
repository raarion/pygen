"""Wizard CLI: menu bertingkat murni Python stdlib (input()/print()).
Ini BUKAN NLP/AI — user memilih dari daftar terbatas di tiap langkah
(decision tree eksplisit), sehingga pencocokan template selalu deterministik.

Struktur wizard:
  1. Pilih domain (jika multi-domain)
  2. Pilih kategori dalam domain
  3. Pilih template dalam kategori
  4. Isi field satu per satu
  5. Generate → ulangi atau simpan
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pygen.core.registry import (
    load_categories,
    get_domains,
    TemplateBankError,
    search_templates,
)
from pygen.core.template_engine import render, FieldValidationError, _is_truthy
from pygen.core.validator import validate_syntax, CodeValidationError
from pygen.core.compositor import compose, GeneratedUnit


def _prompt_choice(prompt_text: str, options: list, show_status: bool = False) -> int:
    """Tampilkan daftar bernomor, minta user pilih. Kembalikan index (0-based).
    Deterministik: hanya menerima angka valid dari daftar yang ditampilkan.
    """
    while True:
        print(f"\n{prompt_text}")
        for i, opt in enumerate(options, start=1):
            label = opt if isinstance(opt, str) else opt.get("label", str(opt))
            # If show_status and opt has 'status', display it
            status = ""
            if isinstance(opt, dict) and opt.get("status"):
                status = f" {opt['status']}"
            print(f"  {i}. {label}{status}")
        raw = input("Pilih nomor: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print("Input tidak valid, coba lagi.")


def _prompt_bool(label: str, default: bool = False) -> bool:
    """Prompt yes/no sederhana."""
    default_str = "Y/n" if default else "y/N"
    raw = input(f"{label} ({default_str}): ").strip().lower()
    if raw == "":
        return default
    if raw in ("y", "yes", "true", "1"):
        return True
    return False


def _prompt_field_value(field: dict, template: dict = None):
    """Prompt user untuk mengisi satu field, dengan penanganan per tipe."""
    ftype = field["type"]
    label = field["label"]
    default = field.get("default")

    hint_map = {
        "identifier": "(nama variabel Python)",
        "text": "(teks bebas)",
        "int": "(angka bulat)",
        "list": "(pisahkan dengan koma, kosongkan jika tidak perlu)",
        "choice": f"(pilih salah satu: {field.get('options', [])})",
        "bool": "",
        "multi_line": "(teks multi-baris, akhiri dengan baris kosong)",
        "args": "(contoh: nama, age: int = 0)",
        "optional": "(teks opsional, kosongkan jika tidak perlu)",
    }

    hint = hint_map.get(ftype, "")

    if ftype == "bool":
        default_bool = default if isinstance(default, bool) else False
        return _prompt_bool(label, default_bool)

    if ftype == "multi_line":
        default_display = str(default) if default else "(kosong)"
        print(f"\n{label} {hint}")
        print(f"[default: {default_display}]")
        print("Ketik konten (akhiri dengan baris kosong):")
        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)
        return "\n".join(lines) if lines else default

    if ftype == "args":
        default_display = str(default) if default else "(kosong)"
        raw = input(f"\n{label} {hint} [default: {default_display}]: ").strip()
        return raw if raw != "" else default

    if ftype == "optional":
        default_display = str(default) if default else "(kosong)"
        raw = input(f"\n{label} {hint} [default: {default_display}]: ").strip()
        return raw if raw != "" else default

    # Default for identifier, text, int, list, choice
    default_display = default
    if isinstance(default, list):
        default_display = ", ".join(default) if default else "(kosong)"
    elif default is None or default == "":
        default_display = "(kosong)"

    raw = input(f"\n{label} {hint} [default: {default_display}]: ").strip()
    return raw if raw != "" else default


def _collect_field_values(template: dict) -> dict:
    print(f"\n--- Mengisi field untuk: {template['title']} ---")
    description = template.get("description", "")
    if description:
        print(f"{description}")
    values = {}
    for field in template["fields"]:
        values[field["name"]] = _prompt_field_value(field, template)
    return values


def _build_generated_unit(template: dict, code: str) -> GeneratedUnit:
    """Buat GeneratedUnit dari template + code hasil render."""
    requires = template.get("requires", {})
    return GeneratedUnit(
        template_id=template["id"],
        title=template["title"],
        imports=template.get("imports", []),
        code=code,
        requires=requires,
    )


def run_wizard(domain: str = None):
    """Jalankan wizard interaktif. Jika domain diberikan, langsung ke domain itu."""
    print("=" * 60)
    print("  PyGen — Generator Fungsi Python Deterministik")
    print("  (tanpa AI/LLM — 100% berbasis template & aturan tetap)")
    print("=" * 60)

    # Step 0: detect domains
    domains = get_domains()

    if len(domains) > 1 and domain is None:
        domain_idx = _prompt_choice(
            "Pilih domain:",
            [f"{d['label']} ({d['key']})" for d in domains],
        )
        domain = domains[domain_idx]["key"]
    elif domain is None:
        # Single domain: use it automatically
        domain = domains[0]["key"] if domains else None

    try:
        if domain and domain != "__root__":
            categories = load_categories(domain=domain)
        else:
            categories = load_categories()
    except TemplateBankError as e:
        print(f"\n[FATAL] Bank data template bermasalah: {e}")
        return

    generated_units = []

    while True:
        cat_idx = _prompt_choice(
            "Pilih kategori fungsi yang ingin dibuat:",
            [f"{c['label']}" for c in categories],
        )
        category = categories[cat_idx]

        tpl_idx = _prompt_choice(
            f"Pilih fungsi dari kategori '{category['label']}':",
            [f"{t['title']}" for t in category["templates"]],
        )
        template = category["templates"][tpl_idx]

        values = _collect_field_values(template)

        try:
            code = render(template, values)
            validate_syntax(code, context_label=template["title"])
        except (FieldValidationError, CodeValidationError) as e:
            print(f"\n[ERROR] {e}")
            print("Fungsi ini dibatalkan, silakan coba lagi dari menu.")
            continue

        print("\n--- Kode dihasilkan ---")
        print(code)

        generated_units.append(_build_generated_unit(template, code))

        again = _prompt_choice(
            "Mau tambah fungsi lain untuk dirangkai jadi satu file?",
            ["Ya, pilih fungsi lain", "Tidak, selesai dan simpan file"],
        )
        if again == 1:
            break

    if not generated_units:
        print("\nTidak ada fungsi yang dihasilkan. Selesai.")
        return

    try:
        final_code = compose(generated_units)
    except CodeValidationError as e:
        print(f"\n[FATAL] Gagal merangkai kode: {e}")
        return

    output_path = input(
        "\nSimpan sebagai file (contoh: my_tools.py) [default: generated_functions.py]: "
    ).strip() or "generated_functions.py"

    if not output_path.endswith(".py"):
        output_path += ".py"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    print(f"\n✅ Selesai. {len(generated_units)} fungsi disimpan ke: {output_path}")
    print("File ini siap dijalankan / diimpor ke proyek lain.")


if __name__ == "__main__":
    run_wizard()
