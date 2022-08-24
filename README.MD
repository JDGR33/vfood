# Food prices scraping for Venezuela

# Description

The aim of the project is to create a package for scraping Food prices from supermarkets in Venezuela. This could include functions to get related information, like the official exchange rate. 

# Installation

# Usage
```python
import vfood.main as fs

#Scrape tomate and leche prices as a pd.DataFrame, delete unrelated 
# results and create a column to show all the 
# prices in US dollars using the official exchange rate
df = fs.scrape_prep_data(["tomate","leche"])

#Scrape the official exchange rate a dictionary 
# with the date, and the source
exchange_info = fs.bcv_exchange_rate()
```


# Roadmap
* Create tests for development
* Scrape unofficial exchange rate

# Contribution 
I am not ready for accepting contributions at the moment, but fell free to give feedback.

# Authors and acknowledgment
Julio Guerrero is the author of this project, his email is juliodanielguerrero@gmail.com.

Special thanks to Gabriel Velasquez for given me the idea for this project.

# License

This project was made with a MIT license, for more information read the LICENSE file.
