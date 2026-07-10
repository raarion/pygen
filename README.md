# PyGen v2

Generator fungsi Python **deterministik** — dari prompt engineering, file processing,
web client, sampai CLI tool scaffold. Tidak ada AI/LLM yang dipanggil di dalam alat ini
sama sekali — semua kode dihasilkan lewat wizard menu bertingkat + bank template yang
sudah diverifikasi, sehingga hasilnya selalu bisa diprediksi dan diulang persis sama.

## Kenapa alat ini?

Nulis boilerplate Python itu repetitif dan rawan typo — dari argparse scaffold,
CSV reader, HTTP client, sampai JSON handler. PyGen menghilangkan beban itu —
kamu jawab beberapa pertanyaan lewat wizard atau via CLI flag, dapat kode
Python siap pakai yang sintaksnya otomatis divalidasi.

## Instalasi

Tidak butuh dependency eksternal — murni Python standard library.

```bash
# Cukup pastikan Python 3.8+ terpasang, lalu langsung jalankan:
python3 -m pygen.cli_entry
```

Atau install sebagai package:

```bash
pip install -e .
pygen
```

## Cara Pakai

### Wizard Interaktif

```bash
pygen                       # wizard penuh (akan tanya domain dulu)
pygen --domain data         # wizard langsung ke domain File & Data
```

### Mode Cepat (non-interaktif)

```bash
pygen --search "csv"                           # cari template
pygen --list                                   # list semua 44 template
pygen --domains                                # list semua domain
pygen --batch csv_reader write_json_file       # generate tanpa prompt
pygen --batch read_csv -v '{"nama_fungsi":"load_data"}'  # dengan values custom
```

### Wizard Step-by-Step

1. Jalankan wizard (`pygen`).
2. Pilih domain (Prompt Engineering / File & Data / Web & Network / CLI).
3. Pilih kategori dalam domain.
4. Pilih template spesifik.
5. Isi field — tipe yang didukung: identifer, text, int, list, choice,
   **bool**, **multi_line**, **args**, **optional**.
6. Kode ditampilkan + divalidasi syntax (`ast.parse`).
7. Bisa tambah fungsi lain, atau langsung simpan file `.py`.

## Domain & Template (44 template, 4 domain)

| Domain | Kategori | Template |
|---|---|---|
| **Prompt Engineering** | API & Koneksi LLM | generic_api_caller, retry_handler, multi_provider_switcher |
| | Embeddings | embedding_fetcher, cosine_similarity, simple_vector_store |
| | Error Handling | llm_exception_hierarchy, circuit_breaker, fallback_chain |
| | Evaluasi | rubric_scorer, llm_as_judge, comparison_ranker |
| | Iterasi & Testing | prompt_ab_tester, batch_runner, simple_logger |
| | Output Handling | json_extractor, output_validator, retry_on_invalid_output |
| | Prompt Chaining | linear_chain, context_passing, branching |
| | Prompt Construction | template_filler, few_shot_builder, message_composer |
| | Streaming | sse_stream_reader, stream_collector, chunked_http_reader |
| | Utilitas | token_estimator, cost_estimator, conversation_history |
| **File & Data** | CSV Tools | csv_reader, csv_writer |
| | File Operations | read_text_file, write_text_file |
| | JSON Tools | read_json_file, write_json_file |
| **Web & Network** | HTTP Client | http_get, http_post_json |
| | Web Scraping | html_link_extractor, simple_downloader |
| **CLI & Automation** | Argparse Scaffold | cli_tool_scaffold, argparse_typed_args |
| | Subprocess | run_command, background_worker |

## Struktur Proyek

```
pygen/
├── pygen/
│   ├── core/
│   │   ├── registry.py          # multi-domain loader + lazy load + search
│   │   ├── template_engine.py   # render {{field}}, conditional blocks {{#field}}
│   │   ├── validator.py         # ast.parse() — gerbang keamanan sintaks
│   │   └── compositor.py        # gabung fungsi + auto requirements header
│   ├── templates/               # BANK DATA per domain
│   │   ├── prompt_eng/
│   │   │   ├── _meta.json
│   │   │   ├── api_connection.json
│   │   │   └── ...
│   │   ├── data/
│   │   │   ├── _meta.json
│   │   │   ├── csv_tools.json
│   │   │   ├── file_ops.json
│   │   │   └── json_tools.json
│   │   ├── web/
│   │   │   ├── _meta.json
│   │   │   ├── http_client.json
│   │   │   └── scraping.json
│   │   └── cli/
│   │       ├── _meta.json
│   │       ├── argparse_scaffold.json
│   │       └── subprocess.json
│   ├── wizard/
│   │   └── cli.py               # menu bertingkat (decision tree) + domain picker
│   └── cli_entry.py             # entry point + search/list/domains/batch flags
├── tests/
│   └── test_templates.py         # 10 test suite — semua template wajib valid
├── examples/
│   └── example_usage.py          # pakai engine tanpa wizard (programatik)
├── docs/
│   ├── BLUEPRINT.md              # arsitektur & prinsip desain
│   └── CONTRIBUTING_TEMPLATES.md # cara nambah template & domain baru
└── setup.py
```

## Field Types Lengkap

| Type | Input | Output Contoh |
|---|---|---|
| `identifier` | nama variabel Python | `read_csv` |
| `text` | teks bebas | `"hello world"` |
| `int` | angka bulat | `30` |
| `list` | comma-separated | `["a", "b", "c"]` |
| `choice` | pilih dari opsi | `True` |
| `bool` | yes/no → True/False | `True` |
| `multi_line` | teks multi-baris (akhiri baris kosong) | `"""docstring"""` |
| `args` | parameter fungsi | `name, age: int = 0, *flags` |
| `optional` | teks opsional, kosong → skip | (varies) |

## Conditional Blocks

Gunakan `{{#fieldname}}...{{/fieldname}}` untuk menyembunyikan bagian kode
saat field kosong / False:

```json
{
  "code": "def greet(name):\n    print('Hello'){{#verbose}}\n    print('Debug: processing'){{/verbose}}"
}
```

## Menambah Template Baru

1. Buat file `.json` di sub-folder domain, atau buat domain baru dengan folder + file `_meta.json`.
2. Ikuti skema: `category`, `label`, `templates` — tiap template wajib punya `sample_values`.
3. Jalankan `python tests/test_templates.py` untuk validasi.
4. Optional: tambah `"requires": {"python": ">=3.10", "packages": ["requests"]}` per template.

## Menjalankan Test

```bash
python tests/test_templates.py
```

10 test termasuk: validasi semua template, cek placeholder tak tersisa,
composite seluruh template jadi satu file, lazy load per domain, search,
dan batch workflow.

## Prinsip Inti

- **Deterministik** — tidak ada randomness, tidak ada model bahasa.
- **Selection, bukan guessing** — user memilih dari menu / search by keyword.
- **Aman** — tidak pernah `eval()`/`exec()` input user; `ast.parse()` setiap output.
- **Data-driven** — nambah kemampuan = nambah JSON, bukan nambah kode.
- **Multi-domain** — 4 domain siap pakai, extensible via sub-folder.
