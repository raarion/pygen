from setuptools import setup, find_packages

setup(
    name="pygen",
    version="2.0.0",
    description="Generator fungsi Python deterministik (tanpa AI internal). Multi-domain: prompt engineering, data, web, CLI.",
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    package_data={
        "pygen": [
            "templates/**/*.json",
            "templates/**/_meta.json",
        ]
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pygen=pygen.cli_entry:main",
        ],
    },
)
