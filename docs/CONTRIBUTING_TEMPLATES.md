# Cara Menambah Template Baru

Template = data, bukan kode. Tambahkan tanpa menyentuh `pygen/core/`.

## Langkah

1. Buka file kategori yang sesuai di `pygen/templates/`, atau buat file
   kategori baru `pygen/templates/nama_kategori.json` dengan isi awal:
   ```json
   { "category": "nama_kategori", "label": "Nama Tampilan Kategori", "templates": [] }
   ```
2. Tambahkan objek template baru ke dalam array `templates`:
   ```json
   {
     "id": "id_unik_snake_case",
     "title": "Judul singkat, tampil di menu",
     "description": "1-2 kalimat, jelas dan konkret",
     "imports": ["modul_stdlib_yang_dibutuhkan"],
     "fields": [
       {"name": "nama_fungsi", "label": "Nama fungsi", "type": "identifier", "default": "my_func"}
     ],
     "code": "def {{nama_fungsi}}():\n    pass\n",
     "sample_values": {"nama_fungsi": "my_func"}
   }
   ```
3. **Wajib**: isi `sample_values` untuk SEMUA field — dipakai test otomatis.
4. Placeholder di `code` HARUS pakai kurung kurawal ganda `{{nama_field}}`.
   Kurung kurawal tunggal (`{`, `}`) aman dipakai bebas untuk dict/set/f-string
   Python biasa karena renderer hanya mencari pola ganda.
5. Jalankan test:
   ```bash
   python -m pytest tests/test_templates.py -v
   ```
   Semua template harus lolos `ast.parse()` dengan `sample_values`-nya.
6. Hindari:
   - Import pihak ketiga yang tidak ada di stdlib kecuali didokumentasikan
     jelas di `description` (mis. "butuh `pip install requests`").
   - Kode yang memanggil `eval`/`exec`/`os.system` dengan input mentah user.
   - Efek samping tersembunyi yang tidak jelas dari nama fungsi.

## Prinsip kualitas template

- Satu template = satu tanggung jawab jelas (single responsibility).
- Field sesedikit mungkin — hanya yang benar-benar mengubah perilaku inti.
- Default value harus membuat fungsi langsung bisa dijalankan tanpa error
  begitu di-generate (zero-config runnable).
