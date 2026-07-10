"""Validator: memastikan kode hasil render benar-benar valid secara sintaks
Python SEBELUM ditunjukkan ke user. Ini gerbang keamanan & kualitas terakhir —
kode yang gagal parse tidak pernah boleh sampai ke tangan user.

Catatan: ast.parse() hanya MEMERIKSA sintaks, tidak MENGEKSEKUSI kode apapun.
Ini aman dipakai untuk validasi tanpa risiko menjalankan kode sembarangan.
"""

import ast


class CodeValidationError(Exception):
    """Dilempar jika kode hasil render tidak valid secara sintaks Python."""


def validate_syntax(code: str, context_label: str = "kode"):
    """Cek code dengan ast.parse(). Lempar CodeValidationError kalau gagal.
    Tidak mengeksekusi kode sama sekali.
    """
    try:
        ast.parse(code)
    except SyntaxError as e:
        raise CodeValidationError(
            f"Kode hasil generate untuk '{context_label}' tidak valid secara sintaks: "
            f"{e.msg} (baris {e.lineno})"
        )
    return True
