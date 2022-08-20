from setuptools import setup, find_packages

setup(
    author="Julio Guerrero",
    description="Scrape data from Supermarkets in Venezuela.",
    name="food_price_scraping",
    version="0.1.0",
    packages=find_packages(include=["food_price_scraping", "food_price_scraping.*"]),
    install_requires=["bs4", "pandas", "numpy"],
)
