#!/usr/bin/env python3
"""PyGen Web UI Server — serve the web UI and auto-regenerate catalog.json.

Usage:
  python3 serve.py             # Default: port 8899
  python3 serve.py --port 8080 # Custom port
  python3 serve.py --open      # Auto-open browser

The server serves the entire project directory so index.html can fetch
pygen/webui/catalog.json. On startup it regenerates the catalog from
pygen/templates/ so new templates are picked up automatically.

Run this from the repo root (where index.html lives).
"""

import http.server
import json
import os
import sys
import threading
import time
import webbrowser
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(HERE, 'pygen', 'webui', 'catalog.json')
TEMPLATES_DIR = os.path.join(HERE, 'pygen', 'templates')


def build_catalog():
    """Scan pygen/templates/ and rebuild catalog.json."""
    if not os.path.isdir(TEMPLATES_DIR):
        print(f'[WARN] Templates directory not found: {TEMPLATES_DIR}')
        return False

    catalog = {'domains': [], 'templates': [], 'generated': '', 'template_count': 0}

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
            with open(fp) as f:
                cat = json.load(f)
            cat['_domain'] = domain
            for tpl in cat['templates']:
                tpl['_domain'] = domain
                tpl['_category'] = cat['label']
                tpl['_category_key'] = cat['category']
                catalog['templates'].append(tpl)
                domain_count += 1

        domain_entry['count'] = domain_count
        catalog['domains'].append(domain_entry)

    catalog['generated'] = datetime.now().isoformat(timespec='seconds')
    catalog['template_count'] = len(catalog['templates'])

    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, 'w') as f:
        json.dump(catalog, f, ensure_ascii=False)
    return True


def watch_templates():
    """Poll templates/ every 2s for changes, rebuild catalog if needed."""
    last_mtime = 0
    while True:
        max_mtime = 0
        if os.path.isdir(TEMPLATES_DIR):
            for root, dirs, files in os.walk(TEMPLATES_DIR):
                for f in files:
                    if f.endswith('.json'):
                        mtime = os.path.getmtime(os.path.join(root, f))
                        if mtime > max_mtime:
                            max_mtime = mtime
        if max_mtime > last_mtime and last_mtime > 0:
            print(f'[watch] Template changes detected, rebuilding catalog...')
            if build_catalog():
                with open(CATALOG_PATH) as f:
                    c = json.load(f)
                print(f'[watch] Catalog updated: {c["template_count"]} templates')
        last_mtime = max_mtime
        time.sleep(2)


def main():
    port = 8899
    open_browser = False

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--port' and i < len(sys.argv) - 1:
            port = int(sys.argv[i + 1])
        elif arg == '--open':
            open_browser = True
        elif arg == '--help' or arg == '-h':
            print(__doc__)
            return

    # Build catalog
    if build_catalog():
        with open(CATALOG_PATH) as f:
            c = json.load(f)
        print(f'[catalog] {c["template_count"]} templates from {len(c["domains"])} domains ({os.path.getsize(CATALOG_PATH):,} bytes)')

    # Start file watcher in background
    watcher = threading.Thread(target=watch_templates, daemon=True)
    watcher.start()

    # Serve from repo root
    os.chdir(HERE)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('0.0.0.0', port), handler)

    url = f'http://localhost:{port}'
    print(f'[server] PyGen Web UI → {url}')
    print(f'[server] Serving from: {HERE}')
    print(f'[server] Press Ctrl+C to stop')

    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[server] Shutting down...')
        server.shutdown()


if __name__ == '__main__':
    main()
