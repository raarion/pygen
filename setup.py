from setuptools import setup, find_packages

setup(
    name="promptgen-forge",
    version="1.0.0",
    description="Generator fungsi Python deterministik untuk pemula prompt engineering (tanpa AI internal).",
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    package_data={"promptgen": ["templates/*.json"]},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "promptgen=promptgen.cli_entry:main",
        ],
    },
)
