# 🍑 PyGen v2 — Python Code Generator

> **258 template • 31 domain • 100% deterministic • Zero AI/LLM**

Generator fungsi Python **deterministik** dengan koleksi template terlengkap — dari data structures, algorithms, web development, database, concurrency, testing, hingga machine learning. Semua kode dihasilkan lewat wizard interaktif + bank template yang sudah diverifikasi, sehingga hasilnya selalu bisa diprediksi dan diulang persis sama.

## 🎯 Kenapa PyGen?

Nulis boilerplate Python itu repetitif dan rawan typo — dari argparse scaffold, CSV reader, HTTP client, sampai ML utilities. PyGen menghilangkan beban itu:

- ⚡ **Zero-config** — Semua template langsung runnable dengan default values
- 🔒 **Safety-first** — Tidak pernah `eval()`/`exec()`, selalu `ast.parse()` validation
- 📦 **Stdlib-first** — 95%+ template tanpa dependency eksternal
- 🚀 **Production-ready** — Thread-safe, error handling, logging patterns included

Kamu jawab beberapa pertanyaan lewat wizard atau via CLI flag, dapat kode Python siap pakai yang sintaksnya otomatis divalidasi.

## 🚀 Quick Start

### Instalasi

Tidak butuh dependency eksternal — murni Python standard library.

```bash
# Clone repository
git clone https://github.com/raarion/pygen.git
cd pygen

# Pastikan Python 3.8+ terpasang, lalu langsung jalankan:
python3 -m pygen.cli_entry
```

Atau install sebagai package:

```bash
pip install -e .
pygen
```

### 🎨 Web UI

Nikmati pengalaman visual modern dengan Web UI:

```bash
# Generate catalog dari semua template
python3 build_webui.py

# Jalankan web server
python3 serve.py

# Buka di browser: http://localhost:8899
```

✨ **Features:**
- Glassmorphism design dengan animated background
- Interactive sidebar dengan smooth animations
- Real-time code generation & preview
- Compose multiple functions into one file
- Mobile-friendly responsive layout

### 💻 CLI Usage

#### Wizard Interaktif

```bash
pygen                       # wizard penuh (akan tanya domain dulu)
pygen --domain data         # wizard langsung ke domain File & Data
```

#### Mode Cepat (non-interaktif)

```bash
pygen --search "csv"                           # cari template
pygen --list                                   # list semua 258 template
pygen --domains                                # list semua 31 domain
pygen --batch csv_reader write_json_file       # generate tanpa prompt
pygen --batch read_csv -v '{"nama_fungsi":"load_data"}'  # dengan values custom
```

### 🎯 Wizard Step-by-Step

1. Jalankan wizard (`pygen`).
2. Pilih dari **31 domain** yang tersedia.
3. Pilih kategori dalam domain.
4. Pilih template spesifik.
5. Isi field — tipe yang didukung: `identifier`, `text`, `int`, `list`, `choice`, `bool`, `multi_line`, `args`, `optional`.
6. Kode ditampilkan + divalidasi syntax (`ast.parse`).
7. Bisa tambah fungsi lain, atau langsung simpan file `.py`.

## 🎨 What's Included

PyGen memiliki **258 template** yang terorganisir dalam **31 domain**, mencakup hampir semua use case umum dalam development Python:

### 📊 Statistics

| Category | Domains | Templates |
|----------|---------|-----------|
| **Foundation** | 6 | 60 |
| **System & OS** | 4 | 37 |
| **Web & Network** | 3 | 21 |
| **Database & Storage** | 2 | 16 |
| **Concurrency & Performance** | 2 | 14 |
| **Developer Tools** | 3 | 18 |
| **CLI & Terminal** | 2 | 14 |
| **Multimedia & Documents** | 2 | 10 |
| **Functional & Metaprogramming** | 2 | 14 |
| **Machine Learning** | 1 | 10 |
| **Prompt Engineering** | 1 | 30 |
| **Total** | **31** | **258** |

---

## 🏗️ Domain Overview

### 🧱 Foundation (6 domains)

#### `data_structures` — 10 templates
LRU Cache, TTL Cache, Bidirectional Dict, Priority Queue, Circular Buffer, dan lainnya.

#### `algorithms` — 10 templates
Binary Search, QuickSort, Merge Sort, Levenshtein Distance, Knapsack, LCS, Topological Sort, dan lainnya.

#### `string_tools` — 11 templates
Slug Generator, Smart Truncation, Case Converter, Email/URL Extractor, Text Anonymizer, dan lainnya.

#### `datetime_utils` — 10 templates
Flexible Date Parser, Business Days Calculator, Timezone Converter, Age Calculator, dan lainnya.

#### `math_stats` — 11 templates
Descriptive Statistics, Linear Regression, Correlation, Prime Generator, Combinatorics, dan lainnya.

#### `iter_tools` — 8 templates
Chunked Iterator, Deep Flatten, Batch Processor, Interleave, Unique Preserver, dan lainnya.

---

### 💻 System & OS (4 domains)

#### `filesystem` — 13 templates
Directory Walker, Duplicate Finder, Atomic Write, File Watcher, Temp File Context, dan lainnya.

#### `os_system` — 9 templates
Memory/Disk/CPU Monitor, Platform Info, Signal Handler, PID File Manager, dan lainnya.

#### `config_loader` — 7 templates
TOML/YAML/INI/DOTENV Reader, Layered Config Merger, Config Validator, dan lainnya.

#### `security` — 8 templates
File Hasher, Password Strength Checker, JWT Lite, HTML Sanitizer, Input Sanitizer, dan lainnya.

---

### 🌐 Web & Network (3 domains)

#### `networking` — 8 templates
TCP Server/Client, HTTP Server, Port Scanner, DNS Lookup, IP Validator, dan lainnya.

#### `api_client` — 8 templates
REST Client, OAuth2 Client, Rate Limiter, GraphQL Builder, Circuit Breaker, dan lainnya.

#### `web_frameworks` — 5 templates
Flask Blueprint Generator, FastAPI Router Generator, CORS Helper, Request Validator, dll.

---

### 🗄️ Database & Storage (2 domains)

#### `database` — 8 templates
SQLite CRUD Factory, Connection Pool, Query Builder, Migration Runner, CSV Importer, dll.

#### `serialization` — 8 templates
Safe Pickle, Base64 Tools, Binary Reader, MessagePack Lite, XML/Dict Converter, NDJSON, dll.

---

### ⚡ Concurrency & Performance (2 domains)

#### `concurrency` — 10 templates
Thread/Process Pool, Async Gather, Producer-Consumer, Timeout Context, Debounce/Throttle, dll.

#### `performance` — 4 templates
Timer Decorator, Memoize, Profiler, Benchmark Runner.

---

### 🛠️ Developer Tools (3 domains)

#### `testing` — 6 templates
Mock Factory, Fixture Generator, Assertion Helpers, Random Test Data, Property Testing, dll.

#### `logging` — 6 templates
Structured JSON Logger, Log Rotator, Context Logger, Metrics Collector, Health Check, dll.

#### `debug` — 6 templates
Traceback Formatter, Debug Context, Retry with Jitter, Deprecation Warning, Safe Getattr, dll.

---

### 🎨 CLI & Terminal (2 domains)

#### `terminal_ui` — 8 templates
Progress Bar, Spinner, ASCII Table, Color Text, Confirm Dialog, Multi-Select, Password Prompt, dll.

#### `cli_advanced` — 6 templates
Click/Typer Scaffold Generator, Terminal Width Detector, Pager, Arg Validators, dll.

---

### 📄 Multimedia & Documents (2 domains)

#### `document` — 7 templates
Word Counter, Markdown/HTML to Text, Keyword Extractor, Text Summarizer, Readability Score, dll.

#### `image_utils` — 3 templates
Image Dimensions Reader, Valid Image Checker, Base64 Image Converter.

---

### 🔮 Functional & Metaprogramming (2 domains)

#### `functional` — 6 templates
Pipe Operator, Function Composer, Currying, Partial Application, Maybe/Either Monad.

#### `metaprogramming` — 8 templates
Class Factory, Dataclass Generator, Mixin Composer, Singleton, Observable, Interface Checker, DI Container, dll.

---

### 🤖 Machine Learning (1 domain)

#### `ml_helpers` — 10 templates
Train/Test Split, Confusion Matrix, Classification Report, One-Hot Encoder, K-Fold CV, Scalers, ROC-AUC, Bootstrap, dll.

---

### 💬 Prompt Engineering (1 domain)

#### `prompt_eng` — 30 templates
API Callers, Embedding Tools, Error Handling, Evaluation, Prompt Chaining, Streaming, Cost Estimator, dll.

## 📁 Struktur Proyek

```
pygen/
├── pygen/
│   ├── core/
│   │   ├── registry.py          # 31-domain loader + lazy load + search
│   │   ├── template_engine.py   # render {{field}}, conditional blocks {{#field}}
│   │   ├── validator.py         # ast.parse() — gerbang keamanan sintaks
│   │   └── compositor.py        # gabung fungsi + auto requirements header
│   │
│   ├── templates/               # 258 templates di 31 domain 🎯
│   │   ├── prompt_eng/          # 30 templates — Prompt Engineering
│   │   ├── data_structures/     # 10 templates — LRU Cache, Priority Queue, dll
│   │   ├── algorithms/          # 10 templates — Binary Search, QuickSort, dll
│   │   ├── string_tools/        # 11 templates — Slugify, Anonymizer, dll
│   │   ├── datetime_utils/      # 10 templates — Date Parser, Timezone, dll
│   │   ├── math_stats/          # 11 templates — Statistics, Regression, dll
│   │   ├── iter_tools/          #  8 templates — Chunked, Flatten, dll
│   │   ├── filesystem/          # 13 templates — Dir Walker, Atomic Write, dll
│   │   ├── os_system/           #  9 templates — Memory Monitor, Signal Handler, dll
│   │   ├── config_loader/       #  7 templates — TOML/YAML Reader, Config Merger, dll
│   │   ├── security/            #  8 templates — JWT Lite, Password Checker, dll
│   │   ├── networking/          #  8 templates — TCP Server, Port Scanner, dll
│   │   ├── api_client/          #  8 templates — REST Client, OAuth2, Circuit Breaker, dll
│   │   ├── web_frameworks/      #  5 templates — Flask/FastAPI Generator, dll
│   │   ├── database/            #  8 templates — SQLite CRUD, Migration, dll
│   │   ├── serialization/       #  8 templates — Safe Pickle, MessagePack, dll
│   │   ├── concurrency/         # 10 templates — Thread Pool, Async, Debounce, dll
│   │   ├── performance/         #  4 templates — Timer, Memoize, Profiler, dll
│   │   ├── testing/             #  6 templates — Mock Factory, Fixture Generator, dll
│   │   ├── logging/             #  6 templates — JSON Logger, Metrics Collector, dll
│   │   ├── debug/               #  6 templates — Retry, Traceback Formatter, dll
│   │   ├── terminal_ui/         #  8 templates — Progress Bar, Spinner, Table, dll
│   │   ├── cli_advanced/        #  6 templates — Click/Typer Generator, dll
│   │   ├── document/            #  7 templates — Summarizer, Keyword Extractor, dll
│   │   ├── image_utils/         #  3 templates — Image Reader, Base64 Converter, dll
│   │   ├── functional/          #  6 templates — Pipe, Compose, Maybe Monad, dll
│   │   ├── metaprogramming/     #  8 templates — Singleton, DI Container, dll
│   │   └── ml_helpers/          # 10 templates — Train/Test Split, ROC-AUC, dll
│   │
│   ├── wizard/
│   │   └── cli.py               # Menu bertingkat (decision tree) + domain picker
│   │
│   └── cli_entry.py             # Entry point + search/list/domains/batch flags
│
├── tests/
│   └── test_templates.py        # 10-test suite — semua template wajib valid ✅
│
├── examples/
│   └── example_usage.py         # Pemakaian tanpa wizard (programatik)
│
├── docs/
│   ├── BLUEPRINT.md             # Arsitektur & prinsip desain
│   └── CONTRIBUTING_TEMPLATES.md # Cara menambah template & domain baru
│
├── index.html                   # Web UI
├── build_webui.py               # Build catalog.json dari template
├── serve.py                     # Serve Web UI secara lokal
│
└── setup.py
```

## 🎯 Field Types Lengkap

| Type | Input | Output Contoh |
|------|-------|---------------|
| `identifier` | nama variabel Python | `read_csv` |
| `text` | teks bebas | `"hello world"` |
| `int` | angka bulat | `30` |
| `list` | comma-separated | `["a", "b", "c"]` |
| `choice` | pilih dari opsi | `True` |
| `bool` | yes/no → True/False | `True` |
| `multi_line` | teks multi-baris (akhiri baris kosong) | `"""docstring"""` |
| `args` | parameter fungsi | `name, age: int = 0, *flags` |
| `optional` | teks opsional, kosong → skip | (varies) |

## 🔀 Conditional Blocks

Gunakan `{{#fieldname}}...{{/fieldname}}` untuk menyembunyikan bagian kode saat field kosong / False:

```json
{
  "code": "def greet(name):\n    print('Hello'){{#verbose}}\n    print('Debug: processing'){{/verbose}}"
}
```

## 📝 Menambah Template Baru

1. Buat file `.json` di sub-folder domain, atau buat domain baru dengan folder + file `_meta.json`.
2. Ikuti skema: `category`, `label`, `templates` — tiap template wajib punya `sample_values`.
3. Jalankan `python tests/test_templates.py` untuk validasi.
4. Optional: tambah `"requires": {"python": ">=3.10", "packages": ["requests"]}` per template.

## 🧪 Menjalankan Test

```bash
python tests/test_templates.py
```

10 test termasuk: validasi semua 258 template, cek placeholder tak tersisa, composite seluruh template jadi satu file, lazy load per domain, search, dan batch workflow.

## 🏆 Prinsip Inti

- **Deterministik** — tidak ada randomness, tidak ada model bahasa.
- **Selection, bukan guessing** — user memilih dari menu / search by keyword.
- **Aman** — tidak pernah `eval()`/`exec()` input user; `ast.parse()` setiap output.
- **Data-driven** — nambah kemampuan = nambah JSON, bukan nambah kode.
- **Multi-domain** — 31 domain siap pakai, extensible via sub-folder.
- **Stdlib-first** — minimal dependency, maksimal portabilitas.
- **Zero-config** — semua template runnable dengan default values.

---

<div align="center">

**Built with ❤️**

[Documentation](docs/) • [Contributing Guide](docs/CONTRIBUTING_TEMPLATES.md) • [Blueprint](docs/BLUEPRINT.md)

</div>
