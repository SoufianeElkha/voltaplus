from setuptools import setup, find_packages

setup(
    name="volta_plus",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'pandas',
        'openpyxl'
    ],
)