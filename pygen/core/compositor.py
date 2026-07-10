"""Compositor: menggabungkan beberapa potongan kode hasil generate (masing-
masing dengan daftar import sendiri) menjadi satu file .py yang rapi —
import di-dedup dan diurutkan, tiap fungsi dipisah jelas dengan komentar asal.

Mendukung metadata 'requires' per unit: jika template punya ketergantungan
paket eksternal, compositor akan menambah komentar pip install di header.
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
    """Satu hasil render: kode + metadata asal termasuk dependensi."""

    def __init__(
        self,
        template_id: str,
        title: str,
        imports: list,
        code: str,
        requires: dict = None,
    ):
        self.template_id = template_id
        self.title = title
        self.imports = imports
        self.code = code
        self.requires = requires or {}  # {"python": ">=3.9", "packages": ["requests"]}


def compose(units: list, generate_requirements_header: bool = True) -> str:
    """Gabungkan list GeneratedUnit menjadi satu source file lengkap.
    Import di-dedup dan diurutkan alfabetis. Validasi sintaks di akhir.
    
    Jika generate_requirements_header=True, tambahkan komentar pip install
    untuk semua paket yang dibutuhkan template.
    """
    if not units:
        raise ValueError("Tidak ada unit kode untuk dirangkai")

    all_imports = set()
    all_packages = set()
    min_python_version = None

    for unit in units:
        all_imports.update(unit.imports)
        # Collect package requirements
        req = unit.requires
        if req:
            for pkg in req.get("packages", []):
                all_packages.add(pkg)
            # Track minimum Python version
            py_ver = req.get("python", "")
            if py_ver:
                if min_python_version is None or py_ver > min_python_version:
                    min_python_version = py_ver

    import_lines = "\n".join(f"import {imp}" for imp in sorted(all_imports))

    body_blocks = []
    for unit in units:
        header_info = [f"# --- {unit.title} (template: {unit.template_id})"]
        if unit.requires:
            req_info = unit.requires
            if req_info.get("packages"):
                header_info.append(f"#     requires: {', '.join(req_info['packages'])}")
            if req_info.get("python"):
                header_info.append(f"#     python: {req_info['python']}")
        header_info.append("")
        block = "\n".join(header_info) + f"\n{unit.code.rstrip()}\n"
        body_blocks.append(block)

    header = HEADER_TEMPLATE.format(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        count=len(units),
    )

    # Add requirements comment section
    requirements_comment = ""
    if generate_requirements_header and (all_packages or min_python_version):
        req_lines = []
        if min_python_version:
            req_lines.append(f"# Python {min_python_version}")
        if all_packages:
            req_lines.append(f"# pip install {' '.join(sorted(all_packages))}")
        if req_lines:
            requirements_comment = "# Requirements:\n" + "\n".join(req_lines) + "\n\n"

    parts = [header]
    if requirements_comment:
        parts.append(requirements_comment)
    if import_lines:
        parts.append(import_lines + "\n\n")
    parts.append("\n\n".join(body_blocks))

    final_code = "".join(parts).rstrip() + "\n"

    validate_syntax(final_code, context_label="hasil composite")
    return final_code
