"""Contoh: memakai engine PyGen secara PROGRAMATIK, tanpa wizard
interaktif. Berguna kalau kamu mau integrasikan generator ini ke script
atau tool lain (mis. auto-generate boilerplate saat setup proyek baru).

Demo fitur v2: multi-domain lazy load, search, batch generate + compose.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pygen.core.registry import (
    load_categories,
    get_domains,
    find_template,
    search_templates,
    list_all_template_ids,
)
from pygen.core.template_engine import render
from pygen.core.validator import validate_syntax
from pygen.core.compositor import compose, GeneratedUnit


def main():
    # 1. List semua domain
    print("=== Domain Tersedia ===")
    for d in get_domains():
        print(f"  {d['key']:<20s} {d['label']}")

    # 2. Lazy load: hanya domain 'data'
    print("\n=== Template di domain 'data' ===")
    data_cats = load_categories(domain="data")
    for cat in data_cats:
        for tpl in cat["templates"]:
            print(f"  [{cat['label']}] {tpl['id']} — {tpl['title']}")

    # 3. Search keyword
    print("\n=== Search 'http' ===")
    for tpl in search_templates("http"):
        domain = tpl.get("_domain", "-")
        print(f"  [{domain}] {tpl['id']} — {tpl['title']}")

    # 4. Batch generate: gabung template dari domain berbeda
    print("\n=== Generate & Compose ===")
    all_cats = load_categories()
    units = []

    tpl_ids = ["csv_reader", "http_get", "run_command", "write_json_file"]
    for tid in tpl_ids:
        tpl = find_template(tid, all_cats)
        if tpl is None:
            print(f"  ⚠ Template '{tid}' tidak ditemukan, skip")
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

    final = compose(units)

    output_path = os.path.join(os.path.dirname(__file__), "generated_example.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final)

    domains_used = {u.template_id.split('_')[0] for u in units}
    print(f"  ✅ {len(units)} fungsi dari {len(domains_used)} domain → {output_path}")

    # 5. List total
    ids = list_all_template_ids()
    print(f"\nTotal template tersedia: {len(ids)}")


if __name__ == "__main__":
    main()
