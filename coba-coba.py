"""
File ini dihasilkan otomatis oleh PromptGen Forge.
Dibuat: 2026-07-10T17:07:08
Jumlah fungsi/komponen: 2

PromptGen Forge adalah generator kode deterministik berbasis template —
TIDAK ada AI/LLM yang terlibat dalam pembuatan kode ini.
"""

# --- Pemilih provider LLM (dispatch by name) (template: multi_provider_switcher) ---
PROVIDER_REGISTRY = {}

def register_provider(name):
    """Decorator untuk mendaftarkan fungsi provider baru ke registry."""
    def decorator(func):
        PROVIDER_REGISTRY[name] = func
        return func
    return decorator


def panggil_provider(provider_name, *args, **kwargs):
    """Panggil fungsi provider terdaftar berdasarkan nama string."""
    if provider_name not in PROVIDER_REGISTRY:
        raise ValueError(f"Provider '{provider_name}' belum terdaftar. Tersedia: {list(PROVIDER_REGISTRY)}")
    return PROVIDER_REGISTRY[provider_name](*args, **kwargs)


# --- Bangun prompt few-shot dari contoh (template: few_shot_builder) ---
def build_few_shot_prompt(examples, new_input, input_label="Input", output_label="Output"):
    """examples: list of (input, output) tuple. Kembalikan teks prompt few-shot lengkap."""
    separator = "---"
    blocks = []
    for ex_input, ex_output in examples:
        blocks.append(f"{input_label}: {ex_input}\n{output_label}: {ex_output}")
    body = f"\n{separator}\n".join(blocks)
    return f"{body}\n{separator}\n{input_label}: {new_input}\n{output_label}:"
