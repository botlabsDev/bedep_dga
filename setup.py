from setuptools import setup, find_packages

setup(
    name='Bedep_DGA',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "pytest",
        "Pytest-mock",
        "requests",
        "pandas"
    ],
    entry_points={"console_scripts": [
        "bedep_dga=src.main:main"
    ]}
)
