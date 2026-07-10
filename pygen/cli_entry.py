"""Entry point utama. Jalankan dengan: python -m pygen.cli_entry
atau (setelah install) cukup: pygen

Usage:
  pygen                          # Wizard interaktif penuh
  pygen --domain DATA            # Wizard langsung ke domain tertentu
  pygen --search "csv reader"    # Cari template
  pygen --list                   # List semua template id
  pygen --batch TEMPLATE_ID ...  # Generate non-interaktif (untuk CI/scripting)
  pygen --domains                # List domain yang tersedia
"""

import argparse
import json
import sys

from pygen.wizard.cli import run_wizard
from pygen.core.registry import (
    load_categories,
    get_domains,
    search_templates,
    list_all_template_ids,
    find_template,
    TemplateBankError,
)
from pygen.core.template_engine import render, FieldValidationError
from pygen.core.validator import validate_syntax, CodeValidationError
from pygen.core.compositor import compose, GeneratedUnit


def cmd_search(query: str):
    """Cari template berdasarkan kata kunci."""
    try:
        results = search_templates(query)
    except TemplateBankError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"Tidak ada template yang cocok dengan '{query}'.")
        return

    print(f"Ditemukan {len(results)} template untuk '{query}':\n")
    for tpl in results:
        domain = tpl.get("_domain", "-")
        print(f"  [{domain}] {tpl['id']}")
        print(f"         {tpl['title']}")
        print(f"         {tpl.get('description', '')}")
        print()


def cmd_list():
    """List semua template id."""
    try:
        ids = list_all_template_ids()
    except TemplateBankError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Total template: {len(ids)}\n")
    cats = load_categories()
    for cat in cats:
        domain_str = f" [{cat.get('domain', '')}]" if cat.get("domain") else ""
        print(f"## {cat['label']}{domain_str}")
        for tpl in cat["templates"]:
            print(f"    {tpl['id']:<40s} {tpl['title']}")
        print()


def cmd_domains():
    """List domain yang tersedia."""
    domains = get_domains()
    if not domains:
        print("Tidak ada domain terdeteksi (struktur flat).")
        return
    print(f"Domain ({len(domains)}):\n")
    for d in domains:
        print(f"  {d['key']:<20s} {d['label']}")


def cmd_batch(args):
    """Generate template secara non-interaktif."""
    template_ids = args.batch
    values_json = args.values

    try:
        values_list = json.loads(values_json) if values_json else {}
    except json.JSONDecodeError as e:
        print(f"[ERROR] Nilai JSON tidak valid: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        categories = load_categories(domain=args.domain)
    except TemplateBankError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # If values is a single dict (not a list), apply same values to all templates
    if isinstance(values_list, dict) and not any(isinstance(v, dict) for v in values_list.values()):
        # Single values dict → apply to all requested templates
        values_per_template = {tid: values_list for tid in template_ids}
    elif isinstance(values_list, list):
        # List of {id: ..., values: {...}}
        values_per_template = {}
        for entry in values_list:
            tid = entry.get("id")
            if tid:
                values_per_template[tid] = entry.get("values", {})
        # Fill remaining with defaults
        for tid in template_ids:
            if tid not in values_per_template:
                values_per_template[tid] = {}
    elif isinstance(values_list, dict):
        # Dict of template_id → values
        values_per_template = values_list
        for tid in template_ids:
            if tid not in values_per_template:
                values_per_template[tid] = {}
    else:
        values_per_template = {tid: {} for tid in template_ids}

    units = []
    for tid in template_ids:
        tpl = find_template(tid, categories)
        if tpl is None:
            print(f"[ERROR] Template '{tid}' tidak ditemukan.", file=sys.stderr)
            sys.exit(1)

        vals = values_per_template.get(tid, {})
        try:
            code = render(tpl, vals)
            validate_syntax(code, context_label=tid)
        except (FieldValidationError, CodeValidationError) as e:
            print(f"[ERROR] Gagal render '{tid}': {e}", file=sys.stderr)
            sys.exit(1)

        units.append(GeneratedUnit(
            template_id=tid,
            title=tpl["title"],
            imports=tpl.get("imports", []),
            code=code,
            requires=tpl.get("requires", {}),
        ))

    try:
        final_code = compose(units)
    except CodeValidationError as e:
        print(f"[ERROR] Gagal compose: {e}", file=sys.stderr)
        sys.exit(1)

    output = args.output or "generated_functions.py"
    if not output.endswith(".py"):
        output += ".py"
    with open(output, "w", encoding="utf-8") as f:
        f.write(final_code)

    print(f"✅ {len(units)} fungsi disimpan ke: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="PyGen — Generator Fungsi Python Deterministik",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh:
  pygen                                    # wizard interaktif
  pygen --domain data                      # wizard untuk domain 'data' saja
  pygen --search "csv"                     # cari template yang mengandung "csv"
  pygen --list                             # list semua template tersedia
  pygen --domains                          # list semua domain
  pygen --batch read_csv write_json        # generate 2 template dengan default values
  pygen --batch read_csv -v '{"nama_fungsi":"load_data"}'   # dengan values custom
""",
    )
    parser.add_argument("--domain", "-d", help="Domain yang ingin digunakan (lewati pemilihan domain)")
    parser.add_argument("--search", "-s", help="Cari template berdasarkan kata kunci")
    parser.add_argument("--list", "-l", action="store_true", help="List semua template")
    parser.add_argument("--domains", action="store_true", help="List semua domain tersedia")
    parser.add_argument("--batch", "-b", nargs="+", help="Template ID untuk generate non-interaktif")
    parser.add_argument("--values", "-v", default="{}", help="Nilai field dalam format JSON")
    parser.add_argument("--output", "-o", help="Nama file output (default: generated_functions.py)")

    args = parser.parse_args()

    if args.search:
        cmd_search(args.search)
    elif args.list:
        cmd_list()
    elif args.domains:
        cmd_domains()
    elif args.batch:
        cmd_batch(args)
    else:
        run_wizard(domain=args.domain)


if __name__ == "__main__":
    main()
