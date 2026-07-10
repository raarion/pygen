# PromptGen Forge

Generator fungsi Python **deterministik** untuk pemula yang sedang belajar
*prompt engineering*. Tidak ada AI/LLM yang dipanggil di dalam alat ini
sama sekali — semua kode dihasilkan lewat wizard menu bertingkat + bank
template yang sudah diverifikasi, sehingga hasilnya selalu bisa diprediksi
dan diulang persis sama.

## Kenapa alat ini?

Belajar prompt engineering sering kepentok kebutuhan Python: manggil API,
parsing JSON dari respons model, testing beberapa varian prompt, dsb.
PromptGen Forge menghilangkan beban itu — kamu jawab beberapa pertanyaan
lewat wizard, dapat kode Python siap pakai (dan boleh dibaca-baca buat
belajar pelan-pelan).

## Instalasi

Tidak butuh dependency eksternal — murni Python standard library.

```bash
# Cukup pastikan Python 3.8+ terpasang, lalu langsung jalankan:
python3 -m promptgen.cli_entry
```

Atau install sebagai package (opsional):

```bash
pip install -e .
promptgen
```

## Cara Pakai

1. Jalankan wizard.
2. Pilih kategori (mis. "Output Handling").
3. Pilih fungsi spesifik dari daftar (mis. "Ekstrak JSON dari respons LLM").
4. Isi field yang diminta (atau tekan Enter untuk pakai default).
5. Kode langsung ditampilkan & divalidasi sintaksnya otomatis.
6. Bisa tambah fungsi lain untuk dirangkai jadi satu file, atau langsung
   simpan.
7. File `.py` hasilnya siap dijalankan atau di-`import` ke proyek lain.

## Struktur Proyek

```
promptgen_toolkit/
├── promptgen/
│   ├── core/
│   │   ├── registry.py         # memuat & validasi bank data template
│   │   ├── template_engine.py  # render placeholder {{field}} -> kode
│   │   ├── validator.py        # ast.parse() — gerbang keamanan sintaks
│   │   └── compositor.py       # gabung banyak fungsi jadi satu file
│   ├── templates/               # BANK DATA (edit di sini untuk nambah fungsi)
│   │   ├── api_connection.json
│   │   ├── prompt_construction.json
│   │   ├── output_handling.json
│   │   ├── iteration_testing.json
│   │   └── utilities.json
│   ├── wizard/
│   │   └── cli.py               # menu bertingkat (decision tree)
│   └── cli_entry.py              # entry point
├── tests/
│   └── test_templates.py         # validasi otomatis SELURUH bank data
├── examples/
│   └── example_usage.py          # contoh pakai engine tanpa wizard (programatik)
├── docs/
│   ├── BLUEPRINT.md              # arsitektur & prinsip desain lengkap
│   └── CONTRIBUTING_TEMPLATES.md # cara nambah template baru
├── requirements.txt
├── setup.py
└── README.md
```

## Bank Template Bawaan (15 fungsi, 5 kategori)

| Kategori | Fungsi |
|---|---|
| API & Koneksi LLM | pemanggil API generik, retry+backoff, multi-provider switcher |
| Prompt Construction | template filler, few-shot builder, message composer |
| Output Handling | JSON extractor, schema validator, retry-on-invalid-output |
| Iterasi & Testing | A/B tester prompt, batch runner, logger CSV |
| Utilitas | token estimator, cost estimator, conversation history manager |

## Menambah Template Baru

Lihat `docs/CONTRIBUTING_TEMPLATES.md`. Intinya: tambah entri JSON di
`promptgen/templates/`, isi `sample_values`, jalankan test — tidak perlu
sentuh kode Python inti sama sekali.

## Menjalankan Test

```bash
python -m pytest tests/ -v
# atau tanpa pytest:
python tests/test_templates.py
```

Test ini memvalidasi **setiap** template di bank data: render dengan
`sample_values`, cek sintaks dengan `ast.parse()`, dan pastikan gabungan
semua template tetap valid saat dirangkai jadi satu file.

## Prinsip Inti

- **Deterministik** — tidak ada randomness, tidak ada model bahasa.
- **Selection, bukan guessing** — user memilih dari menu, bukan free-text
  yang "ditebak" sistem.
- **Aman** — tidak pernah `eval()`/`exec()` input user; validasi sintaks
  lewat `ast.parse()` sebelum kode ditunjukkan.
- **Data-driven** — nambah kemampuan = nambah JSON, bukan nambah kode.

Detail lengkap ada di `docs/BLUEPRINT.md`.
