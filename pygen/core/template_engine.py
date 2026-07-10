"""Template Engine: mengubah field values (dari wizard atau sample_values)
menjadi kode Python jadi, dengan substitusi placeholder {{nama_field}}.

Sengaja TIDAK memakai str.format()/f-string untuk merender, karena kode
Python hasil template itu sendiri sering mengandung kurung kurawal tunggal
asli (dict, set, f-string) yang akan bentrok dengan str.format(). Placeholder
memakai kurung kurawal GANDA supaya tidak pernah bentrok dengan sintaks
Python biasa.

Fitur:
- Field types: identifier, text, int, list, choice, bool, multi_line, args, optional
- Conditional blocks: {{#fieldname}}...code if field has value...{{/fieldname}}
"""

import re

PLACEHOLDER_PATTERN = re.compile(r"\{\{(\w+)\}\}")
# Conditional blocks: {{#field}}...body...{{/field}}
# Body hanya ditampilkan jika field punya nilai (truthy / non-empty)
CONDITIONAL_PATTERN = re.compile(r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}", re.DOTALL)


class FieldValidationError(Exception):
    """Dilempar jika nilai yang dimasukkan user tidak sesuai tipe field."""


def _is_truthy(value) -> bool:
    """Cek apakah nilai field dianggap 'ada' untuk conditional block."""
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, bool):
        return value
    if isinstance(value, (list, dict)):
        return len(value) > 0
    if isinstance(value, (int, float)):
        return True
    return bool(value)


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
        return str(raw_value) if raw_value is not None else ""

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

    if ftype == "bool":
        if isinstance(raw_value, bool):
            return str(raw_value)
        v = str(raw_value).strip().lower()
        if v in ("true", "1", "yes", "y"):
            return "True"
        if v in ("false", "0", "no", "n", ""):
            return "False"
        raise FieldValidationError(f"'{name}' harus boolean (True/False), dapat: {raw_value!r}")

    if ftype == "multi_line":
        if raw_value is None:
            return ""
        return str(raw_value)

    if ftype == "args":
        # Parameter fungsi: "nama, age: int = 0, *flags" → langsung disisipkan
        if raw_value is None:
            return ""
        return str(raw_value).strip()

    if ftype == "optional":
        # optional: field yang boleh kosong, disisipkan apa adanya
        if raw_value is None:
            return ""
        return str(raw_value).strip()

    raise FieldValidationError(f"Tipe field tidak dikenal: {ftype}")


def render(template: dict, values: dict) -> str:
    """Render template['code'] dengan values (dict raw, per nama field).
    Field yang tidak ada di values akan pakai default dari definisi field.

    Steps:
    1. Resolve semua field values (coerce + default fallback)
    2. Proses conditional blocks {{#field}}...{{/field}}
    3. Substitusi placeholder {{field}}
    """
    code = template["code"]
    resolved = {}
    raw_resolved = {}

    for field in template["fields"]:
        name = field["name"]
        raw = values.get(name, field["default"])
        raw_resolved[name] = raw
        resolved[name] = coerce_value(field, raw)

    # Step 2: process conditional blocks
    def _conditional_replacer(match):
        key = match.group(1)
        body = match.group(2)
        raw_val = raw_resolved.get(key)
        if _is_truthy(raw_val):
            # Substitusi placeholder di dalam body juga
            return PLACEHOLDER_PATTERN.sub(
                lambda m: resolved.get(m.group(1), m.group(0)),
                body,
            )
        return ""

    code = CONDITIONAL_PATTERN.sub(_conditional_replacer, code)

    # Step 3: substitusi placeholder
    def _substitute(match):
        key = match.group(1)
        if key not in resolved:
            err = "Placeholder {{'" + key + "'}} tidak punya definisi field"
            raise FieldValidationError(err)
        return resolved[key]

    rendered_code = PLACEHOLDER_PATTERN.sub(_substitute, code)
    return rendered_code
