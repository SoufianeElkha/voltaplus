
from setuptools import setup, find_packages

setup(
    name="voltaplus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "pandas",
        "openpyxl",
        "pytest"
    ],
)
