# BLUEPRINT — PromptGen Forge

## 1. Tujuan
Alat CLI yang membantu pemula *prompt engineering* menghasilkan kode Python
siap pakai (pemanggilan API LLM, parsing output, testing prompt, dsb) tanpa
harus menguasai Python dari nol — **tanpa** memanggil AI/LLM sama sekali di
dalam prosesnya sendiri. Semua output 100% deterministik: input sama →
output sama, persis.

## 2. Prinsip Desain (non-negotiable)

1. **Deterministik total.** Tidak ada `random`, tidak ada model bahasa,
   tidak ada heuristik "tebak-tebakan". Pemilihan template terjadi lewat
   *decision tree* eksplisit (menu bertingkat), bukan pencocokan teks bebas.
2. **Selection, bukan generation-by-guessing.** User memilih kategori →
   sub-kategori → template dari daftar terbatas. Sistem tidak pernah
   "mengarang" struktur kode baru; ia hanya mengisi slot pada template yang
   sudah diverifikasi manusia.
3. **Safety by construction.**
   - Tidak pernah `eval()`/`exec()` input user ke dalam logika program.
   - Nilai user hanya disisipkan sebagai *data* ke placeholder `{{field}}`,
     bukan dieksekusi.
   - Setiap kode hasil generate divalidasi dengan `ast.parse()` sebelum
     ditunjukkan ke user — kalau gagal parse, sistem menolak menampilkannya.
4. **Extensible via data, bukan via kode.** Template disimpan sebagai file
   JSON di `promptgen/templates/*.json` (bank data), terpisah total dari
   logic engine (`promptgen/core/*.py`). Menambah kemampuan baru = menambah
   entri JSON, tidak perlu sentuh kode inti.
5. **Composable.** Setiap template mendeklarasikan `imports` miliknya sendiri.
   Compositor menggabungkan beberapa fungsi jadi satu file, dedup import,
   dan tetap valid secara sintaks.
6. **Testable.** Setiap template di bank data wajib punya `sample_values`
   sehingga test suite bisa merender + `ast.parse` seluruh bank secara
   otomatis. Template yang gagal test tidak boleh masuk rilis.

## 3. Arsitektur

```
User
 │
 ▼
Wizard (wizard/cli.py)          ← decision tree, murni Python stdlib (input())
 │  memilih: kategori → template → isi field
 ▼
Registry (core/registry.py)     ← load & validasi semua file JSON di templates/
 │
 ▼
Template Engine (core/template_engine.py)
 │  render(): substitusi {{field}} → nilai user (regex, bukan str.format,
 │            supaya aman terhadap kurung kurawal Python asli seperti dict/set)
 ▼
Validator (core/validator.py)   ← ast.parse(), tolak jika sintaks salah
 │
 ▼
Compositor (core/compositor.py) ← gabung banyak fungsi, dedup import,
 │                                  susun jadi 1 file .py
 ▼
Output: file .py siap pakai / siap ditempel ke proyek lain
```

## 4. Skema Bank Data (`templates/*.json`)

Setiap file kategori berisi list objek template:

```json
{
  "id": "json_extractor",
  "title": "Ekstrak JSON dari respons LLM",
  "description": "Ambil objek JSON dari teks respons model, validasi key wajib.",
  "imports": ["json", "re"],
  "fields": [
    {
      "name": "nama_fungsi",
      "label": "Nama fungsi",
      "type": "identifier",
      "default": "extract_json"
    },
    {
      "name": "expected_keys",
      "label": "Key wajib (pisahkan koma, boleh kosong)",
      "type": "list",
      "default": []
    }
  ],
  "code": "def {{nama_fungsi}}(response_text):\n    ...",
  "sample_values": {"nama_fungsi": "extract_json", "expected_keys": []}
}
```

Field `type` yang didukung: `identifier` (harus valid nama variabel Python),
`text`, `list` (input "a,b,c" → literal list Python), `int`, `choice`.

## 5. Kategori Bank Awal (15 template)

| Kategori | Isi |
|---|---|
| `api_connection` | pemanggil API generik, retry+backoff, multi-provider switcher |
| `prompt_construction` | template filler, few-shot builder, message composer |
| `output_handling` | JSON extractor, schema validator, retry-on-invalid-output |
| `iteration_testing` | A/B tester prompt, batch runner, logger CSV |
| `utilities` | token estimator, cost estimator, conversation history manager |

## 6. Roadmap Perluasan (opsional, tanpa ubah prinsip)
- Tambah kategori `data_pipeline` (loader dataset evaluasi prompt).
- Tambah field `type: "code_snippet"` untuk slot lanjutan (tetap lewat
  whitelist, bukan eval).
- Ekspor riwayat wizard ke file `.promptgen_session.json` supaya user bisa
  reproduce hasil yang sama persis kapan saja (reprodusibilitas penuh).
