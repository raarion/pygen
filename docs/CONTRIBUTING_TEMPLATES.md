# Cara Menambah Template Baru

Template = data, bukan kode. Tambahkan tanpa menyentuh `pygen/core/`.

## Langkah

### Tambah template ke domain existing

1. Buka file kategori yang sesuai di sub-folder domain, misalnya
   `pygen/templates/data/csv_tools.json`, atau buat file kategori baru di folder
   domain yang sama:
   ```json
   { "category": "nama_kategori", "label": "Nama Tampilan Kategori", "templates": [] }
   ```

### Buat domain baru

1. Buat sub-folder baru di `pygen/templates/`, mis. `databases/`.
2. Buat file `_meta.json` di dalamnya:
   ```json
   {"label": "Database Tools"}
   ```
3. Tambahkan file kategori `.json` seperti biasa. Registry akan otomatis
   mendeteksi sub-folder baru sebagai domain.

### Isi template

1. Tambahkan objek template ke dalam array `templates`:
   ```json
   {
     "id": "id_unik_snake_case",
     "title": "Judul singkat, tampil di menu",
     "description": "1-2 kalimat, jelas dan konkret",
     "imports": ["modul_stdlib_yang_dibutuhkan"],
     "requires": {"python": ">=3.9", "packages": ["requests"]},
     "scope": "function",
     "fields": [
       {"name": "nama_fungsi", "label": "Nama fungsi", "type": "identifier", "default": "my_func"},
       {"name": "use_cache", "label": "Gunakan cache?", "type": "bool", "default": false},
       {"name": "custom_docstring", "label": "Docstring custom", "type": "multi_line", "default": ""},
       {"name": "extra_params", "label": "Parameter tambahan", "type": "args", "default": ""}
     ],
     "code": "def {{nama_fungsi}}():{{#custom_docstring}}\n    \"\"\"{{custom_docstring}}\"\"\"{{/custom_docstring}}\n    pass\n",
     "sample_values": {"nama_fungsi": "my_func", "use_cache": false, "custom_docstring": "", "extra_params": ""}
   }
   ```

2. **Wajib**: isi `sample_values` untuk SEMUA field — dipakai test otomatis.

3. Placeholder di `code` HARUS pakai kurung kurawal ganda `{{nama_field}}`.
   Kurung kurawal tunggal (`{`, `}`) aman dipakai bebas untuk dict/set/f-string.

4. Conditional blocks: `{{#field}}...kode...{{/field}}` — body hanya dirender
   jika field punya nilai truthy (tidak kosong, bukan False). Cocok untuk:
   - Optional logging/debug
   - Optional docstring
   - Parameter tambahan yang user bisa kosongkan

5. `requires` metadata (opsional): deklarasikan Python minimum version dan
   external packages. Compositor akan menambah `# Requirements:` header di output.

6. Jalankan test:
   ```bash
   python tests/test_templates.py
   ```
   Semua template harus lolos `ast.parse()` dengan `sample_values`-nya.

## Field Types Lengkap

| Type | Wizard Prompt | Hasil | Contoh Default |
|---|---|---|---|
| `identifier` | `(nama variabel Python)` | string valid identifier | `my_func` |
| `text` | `(teks bebas)` | string | `"hello"` |
| `int` | `(angka bulat)` | integer string | `30` |
| `list` | `(pisahkan koma)` | Python list string | `["a","b"]` |
| `choice` | `(pilih: [opsi])` | salah satu opsi | `","` |
| `bool` | `(Y/n)` | `True` / `False` | `false` |
| `multi_line` | multi-baris, akhiri baris kosong | raw string | `""` |
| `args` | `(contoh: name, age=0)` | raw string disisipkan | `""` |
| `optional` | `(teks opsional)` | raw string / kosong | `""` |

## Hindari

- Import pihak ketiga tanpa `requires.packages`.
- Kode `eval`/`exec`/`os.system` dengan input mentah user.
- `{{` dalam sample_values yang bukan placeholder.
- Efek samping tersembunyi yang tidak jelas dari nama fungsi.

## Prinsip kualitas template

- Satu template = satu tanggung jawab jelas (single responsibility).
- Field sesedikit mungkin — hanya yang benar-benar mengubah perilaku inti.
- Default value harus membuat fungsi langsung bisa dijalankan tanpa error
  begitu di-generate (zero-config runnable).
