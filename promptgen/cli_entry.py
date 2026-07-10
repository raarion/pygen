"""Entry point utama. Jalankan dengan: python -m promptgen.cli_entry
atau (setelah install) cukup: promptgen
"""

from promptgen.wizard.cli import run_wizard


def main():
    run_wizard()


if __name__ == "__main__":
    main()
