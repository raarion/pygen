"""Template Engine: mengubah field values (dari wizard atau sample_values)
menjadi kode Python jadi, dengan substitusi placeholder {{nama_field}}.

Sengaja TIDAK memakai str.format()/f-string untuk merender, karena kode
Python hasil template itu sendiri sering mengandung kurung kurawal tunggal
asli (dict, set, f-string) yang akan bentrok dengan str.format(). Placeholder
memakai kurung kurawal GANDA supaya tidak pernah bentrok dengan sintaks
Python biasa.
"""

import re

PLACEHOLDER_PATTERN = re.compile(r"\{\{(\w+)\}\}")


class FieldValidationError(Exception):
    """Dilempar jika nilai yang dimasukkan user tidak sesuai tipe field."""


def coerce_value(field: dict, raw_value):
    """Ubah raw_value (biasanya string dari input user) menjadi representasi
    kode Python yang akan disisipkan langsung ke dalam source, sesuai type field.
    """
    ftype = field["type"]
    name = field["name"]

    if ftype == "identifier":
        value = str(raw_value).strip()
        if not value:
            raise FieldValidationError(f"'{name}' tidak boleh kosong")
        if not value.isidentifier():
            raise FieldValidationError(
                f"'{name}' harus berupa nama variabel Python yang valid, dapat: {value!r}"
            )
        return value

    if ftype == "text":
        return str(raw_value)

    if ftype == "int":
        try:
            return str(int(raw_value))
        except (TypeError, ValueError):
            raise FieldValidationError(f"'{name}' harus berupa angka bulat, dapat: {raw_value!r}")

    if ftype == "list":
        if isinstance(raw_value, list):
            items = [str(i).strip() for i in raw_value if str(i).strip()]
        else:
            raw_str = str(raw_value).strip()
            items = [i.strip() for i in raw_str.split(",") if i.strip()] if raw_str else []
        return repr(items)

    if ftype == "choice":
        options = field.get("options", [])
        value = str(raw_value).strip()
        if options and value not in options:
            raise FieldValidationError(f"'{name}' harus salah satu dari {options}, dapat: {value!r}")
        return value

    raise FieldValidationError(f"Tipe field tidak dikenal: {ftype}")


def render(template: dict, values: dict) -> str:
    """Render template['code'] dengan values (dict raw, per nama field).
    Field yang tidak ada di values akan pakai default dari definisi field.
    """
    code = template["code"]
    resolved = {}

    for field in template["fields"]:
        name = field["name"]
        raw = values.get(name, field["default"])
        resolved[name] = coerce_value(field, raw)

    def _substitute(match):
        key = match.group(1)
        if key not in resolved:
            raise FieldValidationError(f"Placeholder {{{{'{key}'}}}} tidak punya definisi field")
        return resolved[key]

    rendered_code = PLACEHOLDER_PATTERN.sub(_substitute, code)
    return rendered_code
