"""Contoh: memakai engine PromptGen Forge secara PROGRAMATIK, tanpa wizard
interaktif. Berguna kalau kamu mau integrasikan generator ini ke script
atau tool lain (mis. auto-generate boilerplate saat setup proyek baru).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptgen.core.registry import load_categories, find_template
from promptgen.core.template_engine import render
from promptgen.core.validator import validate_syntax
from promptgen.core.compositor import compose, GeneratedUnit


def main():
    categories = load_categories()

    # Lihat semua kategori & template yang tersedia
    print("Kategori tersedia:")
    for cat in categories:
        print(f"  - {cat['label']} ({len(cat['templates'])} fungsi)")

    # Ambil satu template spesifik langsung by id (tanpa lewat menu wizard)
    tpl_json = find_template("json_extractor", categories)
    tpl_msg = find_template("message_composer", categories)
    tpl_cost = find_template("cost_estimator", categories)

    # Render tiap template dengan nilai custom
    code_json = render(tpl_json, {
        "nama_fungsi": "parse_llm_answer",
        "expected_keys": ["intent", "confidence"],
    })
    code_msg = render(tpl_msg, {"nama_fungsi": "build_chat_messages"})
    code_cost = render(tpl_cost, {"nama_fungsi": "hitung_biaya_prompt"})

    # Validasi tiap potongan (opsional, compose() sudah validasi ulang di akhir)
    for label, code in [("json", code_json), ("msg", code_msg), ("cost", code_cost)]:
        validate_syntax(code, context_label=label)

    # Rangkai jadi satu file
    units = [
        GeneratedUnit(tpl_json["id"], tpl_json["title"], tpl_json["imports"], code_json),
        GeneratedUnit(tpl_msg["id"], tpl_msg["title"], tpl_msg["imports"], code_msg),
        GeneratedUnit(tpl_cost["id"], tpl_cost["title"], tpl_cost["imports"], code_cost),
    ]
    final_code = compose(units)

    output_path = os.path.join(os.path.dirname(__file__), "generated_example.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    print(f"\nBerhasil menghasilkan 3 fungsi tanpa wizard interaktif -> {output_path}")


if __name__ == "__main__":
    main()
