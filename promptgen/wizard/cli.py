"""Wizard CLI: menu bertingkat murni Python stdlib (input()/print()).
Ini BUKAN NLP/AI — user memilih dari daftar terbatas di tiap langkah
(decision tree eksplisit), sehingga pencocokan template selalu deterministik.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from promptgen.core.registry import load_categories, TemplateBankError
from promptgen.core.template_engine import render, FieldValidationError
from promptgen.core.validator import validate_syntax, CodeValidationError
from promptgen.core.compositor import compose, GeneratedUnit


def _prompt_choice(prompt_text: str, options: list) -> int:
    """Tampilkan daftar bernomor, minta user pilih. Kembalikan index (0-based).
    Deterministik: hanya menerima angka valid dari daftar yang ditampilkan.
    """
    while True:
        print(f"\n{prompt_text}")
        for i, opt in enumerate(options, start=1):
            print(f"  {i}. {opt}")
        raw = input("Pilih nomor: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print("Input tidak valid, coba lagi.")


def _prompt_field_value(field: dict):
    ftype = field["type"]
    label = field["label"]
    default = field["default"]
    hint = {
        "identifier": "(nama variabel Python)",
        "text": "(teks bebas)",
        "int": "(angka bulat)",
        "list": "(pisahkan dengan koma, kosongkan jika tidak perlu)",
        "choice": f"(pilih salah satu: {field.get('options', [])})",
    }.get(ftype, "")
    default_display = default if default != [] else "(kosong)"
    raw = input(f"{label} {hint} [default: {default_display}]: ").strip()
    return raw if raw != "" else default


def _collect_field_values(template: dict) -> dict:
    print(f"\n--- Mengisi field untuk: {template['title']} ---")
    print(f"{template['description']}")
    values = {}
    for field in template["fields"]:
        values[field["name"]] = _prompt_field_value(field)
    return values


def run_wizard():
    print("=" * 60)
    print("  PromptGen Forge — Generator Fungsi Python Deterministik")
    print("  (tanpa AI/LLM — 100% berbasis template & aturan tetap)")
    print("=" * 60)

    try:
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

        generated_units.append(
            GeneratedUnit(
                template_id=template["id"],
                title=template["title"],
                imports=template["imports"],
                code=code,
            )
        )

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
        "\nSimpan sebagai file (contoh: my_prompt_tools.py) [default: generated_functions.py]: "
    ).strip() or "generated_functions.py"

    if not output_path.endswith(".py"):
        output_path += ".py"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    print(f"\n✅ Selesai. {len(generated_units)} fungsi disimpan ke: {output_path}")
    print("File ini siap dijalankan / diimpor ke proyek lain.")


if __name__ == "__main__":
    run_wizard()
