from setuptools import setup, find_packages

setup(
    name="pygen",
    version="1.0.0",
    description="Generator fungsi Python deterministik untuk pemula prompt engineering (tanpa AI internal).",
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    package_data={"pygen": ["templates/*.json"]},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pygen=pygen.cli_entry:main",
        ],
    },
)
