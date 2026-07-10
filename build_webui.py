#!/usr/bin/env python3
"""Build pygen/webui/catalog.json from pygen/templates/

The catalog is fetched at runtime by index.html. Run this whenever
templates change so the catalog stays in sync. The serve.py script
also auto-regenerates when it detects file changes.

Usage:
  python3 build_webui.py
"""

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(HERE, 'pygen', 'templates')
CATALOG_PATH = os.path.join(HERE, 'pygen', 'webui', 'catalog.json')


def build_catalog():
    if not os.path.isdir(TEMPLATES_DIR):
        print(f'Error: templates directory not found: {TEMPLATES_DIR}')
        return False

    catalog = {'domains': [], 'templates': [], 'generated': '', 'template_count': 0}
    total_templates = 0

    for domain in sorted(os.listdir(TEMPLATES_DIR)):
        path = os.path.join(TEMPLATES_DIR, domain)
        if not os.path.isdir(path) or domain.startswith('.'):
            continue
        meta_path = os.path.join(path, '_meta.json')
        label = domain
        if os.path.isfile(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
                label = meta.get('label', domain)

        domain_entry = {'key': domain, 'label': label, 'count': 0}
        domain_count = 0

        for fname in sorted(os.listdir(path)):
            if not fname.endswith('.json') or fname.startswith('_'):
                continue
            fp = os.path.join(path, fname)
            try:
                with open(fp) as f:
                    cat = json.load(f)
            except json.JSONDecodeError as e:
                print(f'Warning: skipping {fp} — invalid JSON: {e}')
                continue

            cat['_domain'] = domain
            for tpl in cat['templates']:
                tpl['_domain'] = domain
                tpl['_category'] = cat['label']
                tpl['_category_key'] = cat['category']
                catalog['templates'].append(tpl)
                domain_count += 1
                total_templates += 1

        domain_entry['count'] = domain_count
        catalog['domains'].append(domain_entry)

    catalog['generated'] = datetime.now().isoformat(timespec='seconds')
    catalog['template_count'] = total_templates

    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, 'w') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    size = os.path.getsize(CATALOG_PATH)
    print(f'Catalog: {total_templates} templates in {len(catalog["domains"])} domains ({size:,} bytes) → {CATALOG_PATH}')
    return True


if __name__ == '__main__':
    build_catalog()
