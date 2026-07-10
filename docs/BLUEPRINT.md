# BLUEPRINT — PyGen v2

## 1. Tujuan
Alat CLI yang membantu developer menghasilkan kode Python siap pakai —
dari boilerplate argparse, file processing, HTTP client, sampai prompt
engineering tools — **tanpa** memanggil AI/LLM sama sekali di dalam prosesnya.
Semua output 100% deterministik: input sama → output sama, persis.

## 2. Prinsip Desain (non-negotiable)

1. **Deterministik total.** Tidak ada `random`, tidak ada model bahasa,
   tidak ada heuristik "tebak-tebakan". Pemilihan template terjadi lewat
   *decision tree* eksplisit (menu bertingkat), bukan pencocokan teks bebas.
2. **Selection, bukan generation-by-guessing.** User memilih domain →
   kategori → template dari daftar terbatas. Sistem tidak pernah
   "mengarang" struktur kode baru; ia hanya mengisi slot pada template
   yang sudah diverifikasi manusia.
3. **Safety by construction.**
   - Tidak pernah `eval()`/`exec()` input user ke dalam logika program.
   - Nilai user hanya disisipkan sebagai *data* ke placeholder `{{field}}`,
     bukan dieksekusi.
   - Setiap kode hasil generate divalidasi dengan `ast.parse()` sebelum
     ditunjukkan ke user — kalau gagal parse, sistem menolak menampilkannya.
4. **Extensible via data, bukan via kode.** Template disimpan sebagai file
   JSON di sub-folder per domain, terpisah total dari logic engine
   (`pygen/core/*.py`). Menambah kemampuan baru = menambah entri JSON,
   tidak perlu sentuh kode inti.
5. **Composable.** Setiap template mendeklarasikan `imports` miliknya sendiri.
   Compositor menggabungkan beberapa fungsi jadi satu file, dedup import,
   menambah header `requires` otomatis, dan tetap valid secara sintaks.
6. **Testable.** Setiap template di bank data wajib punya `sample_values`
   sehingga test suite bisa merender + `ast.parse` seluruh bank secara
   otomatis. Template yang gagal test tidak boleh masuk rilis.
7. **Multi-domain via sub-folder.** Setiap domain = satu sub-folder di
   `templates/` dengan file `_meta.json` untuk metadata label.

## 3. Arsitektur

```
User
 │
 ├─(CLI flags)── pygen --search / --list / --domains / --batch
 │
 └─(Wizard)──→ Wizard (wizard/cli.py)         ← decision tree + domain picker
     │  memilih: domain → kategori → template → isi field
     ▼
   Registry (core/registry.py)                ← multi-domain loader, lazy load, search
     │  load_categories(domain="data")        ← hanya load domain yang dipilih
     ▼
   Template Engine (core/template_engine.py)
     │  render(): substitusi {{field}} + conditional {{#field}}...{{/field}}
     │  Field types: identifier, text, int, list, choice, bool,
     │               multi_line, args, optional
     ▼
   Validator (core/validator.py)              ← ast.parse(), tolak jika sintaks salah
     │
     ▼
   Compositor (core/compositor.py)            ← gabung fungsi, dedup import,
     │                                           auto requirements header
     ▼
   Output: file .py siap pakai / siap ditempel ke proyek lain
```

## 4. Struktur Bank Data

```
templates/
├── prompt_eng/
│   ├── _meta.json              → {"label": "Prompt Engineering"}
│   ├── api_connection.json
│   ├── embeddings.json
│   └── ...
├── data/
│   ├── _meta.json              → {"label": "File & Data"}
│   ├── csv_tools.json
│   ├── file_ops.json
│   └── json_tools.json
├── web/
│   ├── _meta.json              → {"label": "Web & Network"}
│   ├── http_client.json
│   └── scraping.json
└── cli/
    ├── _meta.json              → {"label": "CLI & Automation"}
    ├── argparse_scaffold.json
    └── subprocess.json
```

## 5. Skema Template (diperluas untuk v2)

```json
{
  "category": "csv_tools",
  "label": "CSV Tools",
  "templates": [
    {
      "id": "csv_reader",
      "title": "CSV Reader — baca CSV ke list of dict",
      "description": "Baca file CSV dengan header baris pertama...",
      "imports": ["csv"],
      "requires": {"python": ">=3.8", "packages": []},
      "scope": "function",
      "fields": [
        {"name": "nama_fungsi", "label": "Nama fungsi", "type": "identifier", "default": "read_csv"},
        {"name": "delimiter", "label": "Delimiter", "type": "choice", "options": [",", ";", "\\t", "|"], "default": ","}
      ],
      "code": "def {{nama_fungsi}}(filepath):\n    ...",
      "sample_values": {"nama_fungsi": "read_csv", "delimiter": ","}
    }
  ]
}
```

### Field Types (v2)

| Type | Deskripsi | Output |
|---|---|---|
| `identifier` | Nama variabel Python valid | `read_csv` |
| `text` | Teks bebas | `"hello"` |
| `int` | Angka bulat | `30` |
| `list` | Comma-separated → Python list literal | `["a", "b"]` |
| `choice` | Pilih dari `options[]` | (salah satu) |
| `bool` | true/false → Python boolean | `True` / `False` |
| `multi_line` | Teks multi-baris (wizard: akhiri baris kosong) | raw string |
| `args` | Parameter fungsi langsung disisipkan | `name, age: int = 0` |
| `optional` | Boleh kosong, disisipkan apa adanya | raw string |

### Conditional Blocks

```json
{
  "code": "def greet():\n    print('Hello'){{#verbose}}\n    print('Debug'){{/verbose}}"
}
```

`{{#verbose}}...{{/verbose}}` hanya dirender jika field `verbose` punya nilai truthy.
Cocok untuk: conditional logging, optional parameters, toggle konfigurasi.

### Requires Metadata

Template bisa mendeklarasikan ketergantungan:

```json
{
  "requires": {"python": ">=3.9", "packages": ["requests", "rich"]}
}
```

Compositor akan otomatis menambah header `# Requirements:` di file output.

## 6. Lazy Loading per Domain

Registry v2 mendukung lazy loading: `load_categories(domain="data")` hanya
memuat template dari `templates/data/`. Ini memungkinkan ratusan template
tanpa membebani startup.

Fungsi registry baru:
- `get_domains()` — list domain yang tersedia (baca `_meta.json`)
- `load_categories(domain="web")` — lazy load satu domain
- `load_categories()` — load semua (backward compat)
- `search_templates("csv")` — cari keyword case-insensitive
- `list_all_template_ids()` — semua id
- `find_template("csv_reader")` — cari by id

## 7. CLI Multi-Mode

| Mode | Command |
|---|---|
| Wizard penuh | `pygen` |
| Wizard per domain | `pygen --domain data` |
| Search | `pygen --search "http"` |
| List semua | `pygen --list` |
| List domain | `pygen --domains` |
| Batch (CI/script) | `pygen --batch csv_reader write_json_file -v '{"nama_fungsi":"load"}' -o output.py` |

## 8. Roadmap Mendatang
- Ekspor riwayat wizard ke `.pygen_session.json` (reprodusibilitas penuh)
- `--dry-run` mode: tampilkan kode tanpa menyimpan file
- Web UI / TUI alternatif selain `input()` wizard
- Template sharing / registry online
- Negation blocks: `{{^field}}...{{/field}}`
