from setuptools import setup, find_packages

setup(
    author="Julio Guerrero",
    description="Scrape data from Supermarkets in Venezuela.",
    name="vfood",
    version="0.1.0",
    packages=find_packages(include=["vfood", "vfood.*"]),
    install_requires=["bs4", "pandas", "numpy"],
)
