"""Entry point utama. Jalankan dengan: python -m pygen.cli_entry
atau (setelah install) cukup: pygen
"""

from pygen.wizard.cli import run_wizard


def main():
    run_wizard()


if __name__ == "__main__":
    main()
