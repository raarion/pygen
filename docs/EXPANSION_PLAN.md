# PyGen Template Expansion Master Plan

> Current: **44 template, 4 domain, 17 kategori**  
> Target: **200+ template, 12 domain, 50+ kategori**  
> Filosofi: satu template = satu fungsi/tool kecil yang langsung bisa dipakai (zero-config runnable)

---

## State Saat Ini (Baseline)

| Domain | Kategori | Template |
|---|---|---|
| `prompt_eng/` | 10 kategori | 30 |
| `data/` | 3 kategori | 6 |
| `web/` | 2 kategori | 4 |
| `cli/` | 2 kategori | 4 |
| **Total** | **17** | **44** |

Kesenjangan utama: **data structures, algoritma, string processing, date/time, math, filesystem, database, concurrency, logging, config, testing, serialization, security, terminal UI, OS/system** — semuanya belum tersentuh.

---

## Fase 1: Fondasi — Data & Algoritma (6 domain, ~45 template)

Prioritas tertinggi karena ini bahan bangunan paling fundamental.

### 1A. `data_structures/` — Struktur Data

| ID | Judul | Deskripsi |
|---|---|---|
| `lru_cache_dict` | LRU Cache — dict dengan batas kapasitas | Dict yang auto-evict entry paling lama tidak dipakai |
| `ttl_cache_dict` | TTL Cache — dict dengan expiry per key | Dict yang entry-nya expire setelah durasi tertentu |
| `typed_defaultdict` | Typed defaultdict — default value based on type hint | `defaultdict` dengan factory otomatis dari type |
| `ordered_counter` | Ordered Counter — counter yang ingat insertion order | Kombinasi OrderedDict + Counter |
| `bidict` | Bidirectional dict — key↔value lookup dua arah | Dict yang bisa lookup dari key maupun value |
| `deep_merge_dict` | Deep merge — gabung nested dict rekursif | Merge dua dict bersarang tanpa overwrite mentah |
| `dot_access_dict` | DotDict — akses dict dengan dot notation | `d.key.nested` bukan `d["key"]["nested"]` |
| `frozen_dict` | Immutable dict — dict read-only | Dict yang tidak bisa dimodifikasi setelah dibuat |
| `priority_queue` | Priority Queue wrapper — heapq dengan API bersih | Wrapper heapq: push, pop, peek, dengan custom comparator |
| `circular_buffer` | Circular/Ring Buffer — buffer berputar ukuran tetap | Buffer yang overwrite dari awal saat penuh |

### 1B. `algorithms/` — Algoritma

| ID | Judul | Deskripsi |
|---|---|---|
| `binary_search` | Binary search — pencarian biner pada sorted list | Return index atau insertion point |
| `quick_sort` | QuickSort implementation | Implementasi klasik in-place quicksort |
| `merge_sorted` | Merge k sorted list | Gabungkan N buah sorted list jadi satu |
| `levenshtein_distance` | Levenshtein / edit distance | Jarak edit antar dua string (stdlib only) |
| `top_k_frequent` | Top-K frequent elements | K elemen paling sering muncul dari iterable |
| `sliding_window` | Sliding window — max/min/avg window | Window berjalan di atas list angka |
| `two_sum` | Two Sum / hash-map lookup | Cari dua elemen yang jumlahnya = target |
| `knapsack_01` | 0/1 Knapsack — DP sederhana | Dynamic programming knapsack |
| `lcs` | Longest Common Subsequence | LCS dua sequence dengan DP |
| `topological_sort` | Topological sort — Kahn's algorithm | Urutkan DAG secara topologis |

### 1C. `string_tools/` — Pemrosesan String & Teks

| ID | Judul | Deskripsi |
|---|---|---|
| `slugify` | Slug generator — text ke URL-friendly slug | "Halo Dunia!" → "halo-dunia" |
| `truncate_text` | Smart text truncation | Potong teks dengan ellipsis tanpa potong kata |
| `camel_to_snake` | CamelCase ↔ snake_case converter | `MyClass` ↔ `my_class`, bidirectional |
| `remove_accents` | Hapus aksen/diacritics dari teks | "café naïve" → "cafe naive" |
| `extract_emails` | Email extractor dari teks | Regex email dari teks bebas |
| `extract_urls` | URL extractor dari teks | Ekstrak semua URL dari konten |
| `extract_hashtags` | Hashtag & mention extractor | `#python` dan `@user` dari teks |
| `word_wrap` | Word wrap — bungkus teks per kolom | Potong teks panjang ke baris per lebar tertentu |
| `anonymize_text` | Text anonymizer sederhana | Ganti email/phone/name dengan placeholder |
| `diff_strings` | Simple string diff | Bandingkan dua string, output unified diff |
| `str_similarity` | String similarity (Jaccard, Sørensen-Dice) | Hitung kemiripan dua string 0-1 |

### 1D. `datetime_utils/` — Tanggal & Waktu

| ID | Judul | Deskripsi |
|---|---|---|
| `parse_date` | Flexible date parser — multi format | Coba parse "2024-01-01", "01/01/24", "1 Jan 2024" |
| `format_duration` | Format duration — detik ke string | 3661 → "1 jam 1 menit 1 detik" |
| `is_weekend` | Weekend checker | True jika hari Sabtu/Minggu |
| `business_days_between` | Hitung hari kerja antara dua tanggal | Skip weekend (opsional: skip holidays) |
| `add_business_days` | Tambah hari kerja ke tanggal | +5 hari kerja dari hari ini |
| `date_range` | Date range generator | Yield semua tanggal dari A ke B |
| `age_calculator` | Hitung umur dari tanggal lahir | `age("2000-05-15")` → tahun |
| `timezone_converter` | Timezone converter (stdlib: zoneinfo) | Convert UTC ↔ local timezone |
| `iso_week` | ISO week number | Dapatkan ISO week number dari tanggal |
| `next_occurrence` | Next occurrence — 'setiap Senin 9 pagi' | Kapan berikutnya hari X jam Y terjadi? |

### 1E. `math_stats/` — Matematika & Statistik

| ID | Judul | Deskripsi |
|---|---|---|
| `descriptive_stats` | Descriptive statistics — mean, median, mode, stdev | Satu fungsi, semua statistik deskriptif |
| `percentile` | Percentile calculator | Hitung P25, P50, P75, P90 dari list |
| `normalize` | Normalize — min-max & z-score | Normalisasi list ke range 0-1 |
| `moving_average` | Moving / rolling average | SMA dan EMA (exponential) |
| `linear_regression` | Simple linear regression | y = mx + b dari (x,y) pairs |
| `correlation` | Pearson & Spearman correlation | Hitung korelasi antar dua list |
| `factorial` | Factorial (iterative + recursive) | n! dengan kedua metode |
| `prime_generator` | Prime number generator — Sieve of Eratosthenes | Yield bilangan prima sampai N |
| `gcd_lcm` | GCD & LCM calculator | FPB dan KPK |
| `combinatorics` | Combination & permutation generator | `combinations(n,k)` dan `permutations(n,k)` |
| `fibonacci` | Fibonacci sequence generator | Yield deret Fibonacci sampai N |

### 1F. `iter_tools/` — Iterator & Generator Utilities

| ID | Judul | Deskripsi |
|---|---|---|
| `chunked` | Chunked/grouper — pecah iterable per N | `[1,2,3,4,5]` size 2 → `[[1,2],[3,4],[5]]` |
| `flatten` | Deep flatten — ratakan nested iterable | `[1,[2,[3,4]]]` → `[1,2,3,4]` |
| `batch_process` | Batch processor with progress | Proses large iterable per batch |
| `take_until` | Take until condition — yield sampai kondisi true | Stop yield saat predikat terpenuhi |
| `interleave` | Interleave — gabung selang-seling | `interleave([a,b],[1,2])` → `[a,1,b,2]` |
| `unique_everseen` | Unique (seen) — deduplikasi preserve order | Hapus duplikat tanpa mengubah urutan |
| `pairwise` | Pairwise — yield pasangan berurutan | `[1,2,3]` → `[(1,2),(2,3)]` |
| `nth` | Nth element — ambil elemen ke-N dari iterable | Tanpa materialisasi seluruh iterable |

---

## Fase 2: System & OS (4 domain, ~30 template)

### 2A. `filesystem/` — File System Tools

| ID | Judul | Deskripsi |
|---|---|---|
| `dir_walker` | Recursive directory walker | Walk direktori dengan filter extension/size |
| `find_duplicates` | Duplicate file finder | Cari file duplikat berdasarkan hash (MD5/SHA) |
| `dir_size` | Directory size calculator | Hitung total size folder rekursif |
| `glob_matcher` | Advanced glob with regex fallback | Gabungkan glob + regex filter |
| `safe_path` | Path sanitizer — bersihkan karakter ilegal | `/user/na..me/` → `/user/name/` |
| `temp_file_ctx` | Temporary file context manager | with block auto-cleanup temp file |
| `atomic_write` | Atomic file write — tulis aman tanpa corrupt | Tulis ke tmp → rename (POSIX atomic) |
| `file_age` | File age checker | Berapa lama sejak file terakhir dimodifikasi? |
| `split_file` | File splitter — pecah file besar per chunk | Split 1GB file jadi 100MB chunks |
| `merge_files` | File merger — gabung chunks jadi satu | Kebalikan split_file |
| `lock_file` | File-based lock — mutual exclusion | Cegah race condition antar proses |
| `tail_file` | Tail — baca N baris terakhir file | Seperti Unix `tail`, tanpa baca seluruh file |
| `watch_dir` | Simple directory watcher — polling | Deteksi file baru/berubah/hapus di folder |

### 2B. `os_system/` — Sistem Operasi

| ID | Judul | Deskripsi |
|---|---|---|
| `memory_usage` | Current memory usage (RSS) | Memory process saat ini |
| `disk_usage` | Disk usage checker | Free/total disk space |
| `cpu_info` | CPU info & count | Jumlah core, usage percent |
| `process_list` | Running process lister | List proses yang sedang berjalan |
| `env_loader` | Environment variable loader | Baca dan validasi environment variables |
| `platform_info` | Platform detector | OS, architecture, Python version, hostname |
| `signal_handler` | Signal handler helper | Decorator untuk tangkap SIGINT/SIGTERM |
| `pid_file` | PID file manager | Tulis/baca/hapus PID file untuk daemon |
| `which` | which — cari executable di PATH | Seperti Unix `which` command |

### 2C. `config_loader/` — Konfigurasi

| ID | Judul | Deskripsi |
|---|---|---|
| `dotenv_reader` | .env file reader | Baca file .env ke os.environ / dict |
| `ini_reader` | INI/configparser reader | Baca file .ini/.cfg dengan configparser |
| `toml_reader` | TOML reader (stdlib, Python 3.11+) | Baca TOML dengan tomllib |
| `yaml_lite_reader` | YAML-lite reader (tanpa PyYAML) | Baca YAML sederhana dengan regex + ast |
| `config_merger` | Layered config merger | Default → file → env → CLI args |
| `config_validator` | Config schema validator | Validasi config punya key wajib + tipe benar |
| `env_to_config` | ENV prefix to dict | `APP_HOST=...` → `{"host": "..."}` |

### 2D. `security/` — Keamanan & Kriptografi

| ID | Judul | Deskripsi |
|---|---|---|
| `hash_file` | File hasher — MD5/SHA1/SHA256 | Hash file, verifikasi checksum |
| `random_string` | Secure random string generator | Generate token/password random |
| `password_strength` | Password strength checker | Skor kekuatan password + saran |
| `hmac_sign` | HMAC sign & verify | Tanda tangan dan verifikasi dengan HMAC |
| `simple_encrypt` | Simple AES encrypt/decrypt (PyCryptodome/stdlib) | Encrypt/decrypt dengan key |
| `sanitize_html` | HTML sanitizer | Hapus tag berbahaya, sisakan allowed tags |
| `input_sanitizer` | Input sanitizer — anti-injection dasar | Escape karakter khusus untuk SQL/HTML/Shell |
| `jwt_lite` | JWT-lite — encode/decode tanpa library | HS256 encode/decode manual |

---

## Fase 3: Web & Jaringan Lanjutan (3 domain, ~25 template)

### 3A. `networking/` — Jaringan

| ID | Judul | Deskripsi |
|---|---|---|
| `simple_tcp_server` | Simple TCP echo server | Socket server: terima koneksi, echo balik |
| `simple_tcp_client` | Simple TCP client | Socket client: konek ke server, kirim/terima |
| `simple_http_server` | Simple HTTP server — http.server wrapper | Serve static folder, custom handler |
| `port_scanner` | TCP port scanner | Cek port mana yang terbuka di host |
| `dns_lookup` | DNS lookup — A/AAAA/MX records | Resolve hostname ke IP |
| `validate_ip` | IP address validator | Validasi IPv4/IPv6 + cek private/loopback |
| `url_parser` | URL decomposer — parsed URL ke komponen | scheme, host, port, path, query, fragment |
| `is_reachable` | Host reachability checker | TCP connect test ke host:port dengan timeout |

### 3B. `api_client/` — API Client Advanced

| ID | Judul | Deskripsi |
|---|---|---|
| `rest_client_builder` | REST API client builder class | Class dengan .get() .post() .put() .delete() |
| `pagination_handler` | API Pagination handler | Auto-follow next page link / offset pagination |
| `oauth2_client_credentials` | OAuth2 Client Credentials flow | Dapatkan token, simpan, refresh otomatis |
| `api_rate_limiter` | Token bucket rate limiter | Batasi request per detik/menit |
| `graphql_query_builder` | GraphQL query builder | Bangun query/mutation string dari dict Python |
| `bearer_auth_wrapper` | Bearer auth decorator | Auto-attach Authorization header |
| `response_cache` | HTTP response cache | Cache GET response dengan TTL |
| `circuit_breaker_http` | HTTP circuit breaker | Stop panggil API yang gagal berturut-turut |

### 3C. `web_frameworks/` — Web Framework Helpers

| ID | Judul | Deskripsi |
|---|---|---|
| `flask_blueprint_scaffold` | Flask blueprint scaffold | Generate file blueprint + routes |
| `fastapi_router_scaffold` | FastAPI router scaffold | Generate router file dengan CRUD stubs |
| `middleware_timer` | Request timing middleware | WSGI/ASGI middleware: log request duration |
| `cors_headers` | CORS header helper | Generate CORS response headers |
| `request_validator` | Request body/query validator | Validasi request body terhadap schema |

---

## Fase 4: Database & Persistent Storage (2 domain, ~18 template)

### 4A. `database/` — Database (SQLite-First)

| ID | Judul | Deskripsi |
|---|---|---|
| `sqlite_crud_factory` | SQLite CRUD factory — generate class CRUD | Class `UserDB` dengan create/read/update/delete |
| `sqlite_schema_from_dict` | Schema dari dict — auto CREATE TABLE | `{"name":"text","age":"int"}` → SQL CREATE |
| `sqlite_connection_pool` | SQLite connection pool sederhana | Pool koneksi thread-safe |
| `csv_to_sqlite` | CSV → SQLite importer | Baca CSV, auto-create table, bulk insert |
| `sqlite_query_builder` | Simple query builder — select/insert/update/delete | Method chaining: `.select().where().order_by()` |
| `db_migration_runner` | Database migration runner | Jalankan file SQL bermigrasi per versi |
| `sqlite_backup` | SQLite backup helper | Backup database ke file (live backup) |
| `db_seed` | Database seeder | Seed table dengan data dummy |

### 4B. `serialization/` — Serialisasi & Encoding

| ID | Judul | Deskripsi |
|---|---|---|
| `pickle_safe` | Safe pickle — load/dump dengan verifikasi | Pickle dengan hash check anti-tamper |
| `base64_tool` | Base64 encode/decode — string & file | Encode/decode teks atau file |
| `binary_reader` | Binary struct reader — baca binary format | Baca file binary dengan struct format string |
| `msgpack_lite` | MessagePack-lite — encode/decode sederhana | Binary serialization tanpa library |
| `xml_to_dict` | XML → dict converter | Parse XML ke nested dict, stdlib only |
| `dict_to_xml` | Dict → XML converter | Build XML string dari nested dict |
| `csv_dialect_detector` | CSV dialect auto-detector | Deteksi delimiter, quotechar, dll otomatis |
| `line_protocol` | Line protocol — NDJSON / JSONL reader-writer | Baca/tulis file JSON per baris |

---

## Fase 5: Concurrency & Performance (2 domain, ~16 template)

### 5A. `concurrency/` — Konkurensi & Async

| ID | Judul | Deskripsi |
|---|---|---|
| `thread_pool_executor` | Thread pool dengan result collector | Map function ke list, kumpulkan hasil |
| `process_pool_executor` | Process pool — CPU-bound parallel map | Parallel map untuk CPU-heavy task |
| `async_gather` | Async gather — jalankan N coroutine parallel | `async_gather(coro1(), coro2(), coro3())` |
| `producer_consumer` | Producer-Consumer queue | Thread-safe queue: producer → consumer |
| `rate_limited_executor` | Rate-limited async executor | Jalankan task dengan rate limit |
| `timeout_ctx` | Timeout context manager | `with timeout(5): do_work()` |
| `semaphore_limiter` | Semaphore-based concurrency limiter | Batasi N concurrent operations |
| `bounded_executor` | Bounded thread pool — batasi max workers | Pool yang reject saat penuh |
| `debounce` | Debounce decorator | Panggil function hanya setelah idle X detik |
| `throttle` | Throttle decorator | Batasi panggilan function per interval |

### 5B. `performance/` — Performance & Profiling

| ID | Judul | Deskripsi |
|---|---|---|
| `timer_decorator` | Execution timer decorator | Log waktu eksekusi function |
| `memoize` | Memoization decorator | Cache hasil function berdasarkan args |
| `profile_context` | Simple profiler context manager | `with profile():` → print CPU time |
| `benchmark` | Micro-benchmark runner | Jalankan function N kali, return stats |

---

## Fase 6: Developer Tools & Quality (3 domain, ~22 template)

### 6A. `testing/` — Testing & QA Helpers

| ID | Judul | Deskripsi |
|---|---|---|
| `mock_factory` | Mock object factory | Auto-generate mock dengan attributes |
| `fixture_data_generator` | Test fixture data generator | Generate data dummy: user, order, product |
| `assert_helpers` | Assertion helper collection | `assert_approx(a,b)`, `assert_subset`, dll |
| `random_test_data` | Random test data — name, email, phone, address | Generator data realistis untuk testing |
| `property_test_runner` | Property-based test helper | Test invariant: untuk setiap input, properti X terpenuhi |
| `test_suite_runner` | Test suite discovery & runner | Auto-discover test files, run, report |

### 6B. `logging/` — Logging & Monitoring

| ID | Judul | Deskripsi |
|---|---|---|
| `structured_logger` | Structured JSON logger | Log dalam format JSON, bukan plain text |
| `log_rotator` | Log rotation setup helper | Setup RotatingFileHandler otomatis |
| `context_logger` | Context-aware logger — dengan request ID | Logger yang attach correlation ID |
| `metrics_collector` | Simple metrics collector | Counter, gauge, histogram dasar |
| `health_check` | Health check endpoint helper | Return JSON status aplikasi |
| `error_tracker` | Error rate tracker | Track error count + rate per interval |

### 6C. `debug/` — Debugging & Error

| ID | Judul | Deskripsi |
|---|---|---|
| `traceback_formatter` | Pretty traceback formatter | Format exception dengan warna & konteks |
| `debug_context` | Debug context manager — log entry/exit | `with debug_ctx("my_func"):` → log enter/exit |
| `reraise_with_context` | Re-raise exception with context | Wrap exception + tambah info tanpa hilangkan traceback |
| `deprecated_warning` | Deprecation warning decorator | Decorator fungsi deprecated + saran pengganti |
| `retry_with_jitter` | Retry with exponential backoff + jitter | Retry decorator dengan random jitter |
| `safe_getattr` | Safe recursive getattr — tanpa exception | `safe_getattr(obj, "a.b.c", default=None)` |

---

## Fase 7: CLI & Terminal UX (2 domain, ~14 template)

### 7A. `terminal_ui/` — Terminal UI & Visuals

| ID | Judul | Deskripsi |
|---|---|---|
| `progress_bar` | Simple progress bar (ASCII) | `[████░░░░░░] 40%` — stdlib only, no tqdm |
| `spinner` | Spinner context manager | `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` — with block |
| `table_printer` | ASCII table printer | Print list of dict sebagai tabel rapi |
| `color_text` | ANSI color text helper | Print teks berwarna di terminal |
| `confirm_dialog` | Yes/no confirm dialog | Prompt user Y/n dengan default |
| `multi_select` | Multi-select checklist | User pilih beberapa item dari list |
| `password_prompt` | Password input (masked) | Input password dengan karakter tersembunyi |
| `clear_screen` | Clear terminal screen (cross-platform) | Bersihkan layar terminal |

### 7B. `cli_advanced/` — CLI Advanced

| ID | Judul | Deskripsi |
|---|---|---|
| `click_cli_scaffold` | Click CLI scaffold | Generate Click CLI app skeleton |
| `typer_cli_scaffold` | Typer CLI scaffold | Generate Typer CLI dengan type hints |
| `term_width` | Terminal width detector | Dapatkan lebar terminal saat ini |
| `pager_output` | Pager — output panjang dengan scrolling | Pipe output ke less/more otomatis |
| `confirm_overwrite` | Safe overwrite — konfirmasi sebelum overwrite file | Cek file exists → prompt → overwrite |
| `arg_validator` | CLI arg validator — path, url, email, range | Custom argparse type validators |

---

## Fase 8: Multimedia & Dokumen (2 domain, ~12 template)

### 8A. `document/` — Pemrosesan Dokumen

| ID | Judul | Deskripsi |
|---|---|---|
| `word_counter` | Document word/char/line counter | Statistik teks: kata, karakter, baris, paragraf |
| `markdown_to_text` | Markdown → plain text | Strip markdown formatting |
| `html_to_text` | HTML → plain text | Strip HTML tags, decode entities |
| `text_to_blocks` | Split text into paragraph blocks | Pisah teks jadi list paragraf |
| `keyword_extractor` | Simple keyword extractor (TF-based) | Ekstrak keyword dari teks |
| `text_summary` | Text summarizer (extractive) | Ringkasan kalimat paling penting |
| `readability_score` | Readability score — Flesch-Kincaid | Skor keterbacaan teks |

### 8B. `image_utils/` — Gambar (stdlib-only)

| ID | Judul | Deskripsi |
|---|---|---|
| `image_dimensions` | Get image dimensions — width, height, format | Baca metadata gambar (PNG header, JPEG SOF) |
| `is_valid_image` | Validate image file header | Cek magic bytes: PNG, JPEG, GIF, WebP |
| `base64_image` | Image → base64 data URI | Encode gambar ke `data:image/png;base64,...` |

---

## Fase 9: Functional Programming & Metaprogramming (2 domain, ~14 template)

### 9A. `functional/` — Functional Programming

| ID | Judul | Deskripsi |
|---|---|---|
| `pipe` | Pipe operator — `pipe(data, f1, f2, f3)` | Unix pipe style: data lewat serangkaian fungsi |
| `compose` | Function composer — `compose(f,g)(x)` = `f(g(x))` | Komposisi fungsi right-to-left |
| `curry` | Currying decorator | `@curry def add(a,b):` → `add(1)(2)` |
| `partial_right` | Right partial application | Applikan arg dari kanan |
| `maybe` | Maybe monad lite — handle None chain | `Maybe(data).get("key").get("sub")` tanpa NPE |
| `either` | Either monad lite — handle success/error | `Either.success(data)` or `Either.error(msg)` |

### 9B. `metaprogramming/` — Metaprogramming & Code Generation

| ID | Judul | Deskripsi |
|---|---|---|
| `class_factory` | Dynamic class factory | Buat class baru dari dict attributes |
| `dataclass_generator` | Dataclass code generator | Generate `@dataclass` dari field definitions |
| `mixin_composer` | Mixin composer | Gabung beberapa mixin jadi satu class |
| `singleton_metaclass` | Singleton pattern — via metaclass/decorator | Class yang hanya bisa satu instance |
| `observable_property` | Observable property — getter/setter dengan callback | Property dengan onChange event |
| `auto_repr` | __repr__ auto-generator | Decorator: tambah `__repr__` otomatis |
| `interface_checker` | ABC interface validator | Cek class implement semua abstract methods |
| `dep_injector` | Simple dependency injector | Inject dependencies dari registry ke function |

---

## Fase 10: Data Science & ML Helpers (1 domain, ~10 template)

### `ml_helpers/` — Machine Learning Utilities (stdlib)

| ID | Judul | Deskripsi |
|---|---|---|
| `train_test_split` | Train/test split — tanpa sklearn | Split data dengan stratifikasi opsional |
| `confusion_matrix` | Confusion matrix builder | Bangun confusion matrix dari y_true, y_pred |
| `classification_report` | Classification report | Precision, recall, F1 per class |
| `one_hot_encode` | One-hot encoder | Encode categorical ke binary vectors |
| `kfold_split` | K-Fold cross-validation splitter | Generate K fold untuk cross-validation |
| `feature_scaler` | Standard & Min-Max scaler | Normalisasi fitur |
| `r2_score` | R² score calculator | Coefficient of determination |
| `auc_roc` | AUC-ROC calculator (trapezoidal) | Area under ROC curve tanpa sklearn |
| `shuffle_data` | Deterministic data shuffler | Shuffle X,y dengan seed yang sama |
| `bootstrap_sample` | Bootstrap resampling | Generate bootstrap samples untuk confidence interval |

---

## Rangkuman Fase & Estimasi

| Fase | Domain | Kategori Baru | Template |
|---|---|---|---|
| 1 | Fondasi: `data_structures`, `algorithms`, `string_tools`, `datetime_utils`, `math_stats`, `iter_tools` | 6 | 56 |
| 2 | System: `filesystem`, `os_system`, `config_loader`, `security` | 4 | 36 |
| 3 | Web: `networking`, `api_client`, `web_frameworks` | 3 | 21 |
| 4 | Database: `database`, `serialization` | 2 | 16 |
| 5 | Concurrency: `concurrency`, `performance` | 2 | 14 |
| 6 | DevTools: `testing`, `logging`, `debug` | 3 | 17 |
| 7 | Terminal: `terminal_ui`, `cli_advanced` | 2 | 14 |
| 8 | Dokumen: `document`, `image_utils` | 2 | 10 |
| 9 | FP & Meta: `functional`, `metaprogramming` | 2 | 14 |
| 10 | ML: `ml_helpers` | 1 | 10 |
| **Total** | **10 fase, 12 domain baru** | **27** | **208** |

**Total akhir: 44 (existing) + 208 (baru) = 252 template di 16 domain**

## Strategi Eksekusi

1. **Per fase = 1 commit Git**. Satu fase selesai → test → commit → push.
2. **Template dibuat batch 5-10 per file kategori**. Satu file JSON = satu kategori, isi ~5-8 template.
3. **Setiap template wajib `sample_values`**. Test suite (10 test) otomatis memvalidasi.
4. **Prioritas Fase 1 dulu**. Ini fondasi yang paling sering dipakai developer.
5. **Setelah Fase 5**, PyGen sudah mencakup ~80% use case Python umum.
