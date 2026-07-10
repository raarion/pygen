"""Compositor: menggabungkan beberapa potongan kode hasil generate (masing-
masing dengan daftar import sendiri) menjadi satu file .py yang rapi —
import di-dedup dan diurutkan, tiap fungsi dipisah jelas dengan komentar asal.
"""

import datetime

from .validator import validate_syntax

HEADER_TEMPLATE = '''"""
File ini dihasilkan otomatis oleh PyGen.
Dibuat: {timestamp}
Jumlah fungsi/komponen: {count}

PyGen adalah generator kode deterministik berbasis template —
TIDAK ada AI/LLM yang terlibat dalam pembuatan kode ini.
"""

'''


class GeneratedUnit:
    """Satu hasil render: kode + metadata asalnya."""

    def __init__(self, template_id: str, title: str, imports: list, code: str):
        self.template_id = template_id
        self.title = title
        self.imports = imports
        self.code = code


def compose(units: list) -> str:
    """Gabungkan list GeneratedUnit menjadi satu source file lengkap.
    Import di-dedup dan diurutkan alfabetis. Validasi sintaks di akhir.
    """
    if not units:
        raise ValueError("Tidak ada unit kode untuk dirangkai")

    all_imports = set()
    for unit in units:
        all_imports.update(unit.imports)

    import_lines = "\n".join(f"import {imp}" for imp in sorted(all_imports))

    body_blocks = []
    for unit in units:
        block = f"# --- {unit.title} (template: {unit.template_id}) ---\n{unit.code.rstrip()}\n"
        body_blocks.append(block)

    header = HEADER_TEMPLATE.format(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        count=len(units),
    )

    parts = [header]
    if import_lines:
        parts.append(import_lines + "\n\n")
    parts.append("\n\n".join(body_blocks))

    final_code = "".join(parts).rstrip() + "\n"

    validate_syntax(final_code, context_label="hasil composite")
    return final_code
