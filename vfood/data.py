# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:57:22 2021

@author: Julio

This is the module for collecting information of food prices.
"""

import time

# Web Scraping libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError  # For error handling
from urllib.error import URLError  # For error handling

# Data manipulation libraries
import pandas as pd
import regex as re
import numpy as np

# Miscellaneous
from datetime import date  # For getting the Date
from datetime import datetime
import http.client  # For establishing the number of header


# Import utility functions
from scrap import (
    collect_data_global,
    gama_get_products,
    central_m_get_product,
)

http.client._MAXHEADERS = 1000  # Set the limit of headers, more than this will raise an error when using urlopen()


def add_general_columns(
    data: pd.DataFrame, store_name: str, search_term: str
) -> pd.DataFrame:
    """Add a columns for the current date, the name pass as store_name, and the search_term.

    Parameters
    ----------
    data : pd.DataFrame
        The pandas DataFrame resulting from scraping the data from a supermarket web page.

    store_name : str
        The name of the store.

    search_term :
        The name of the prodcut use in the search

    Returns
    -------
    pd.DataFrame :
        A pandas Data Frame with a column with the column date (with the value of the current
        date with %d/%m/%Y format), store_name, and
        search_term.
    """
    assert isinstance(data, pd.DataFrame), f"data must be a pandas DataFrame object"

    data["date"] = date.today().strftime("%d/%m/%Y")
    data["store"] = store_name
    data["search_term"] = search_term

    assert isinstance(data, pd.DataFrame), f"data must be a pandas DataFrame object"
    return data


def bcv_exchange_rate() -> dict:
    """Get the Exchange Rate $/Bs from BCV.

    Returns
    -------
    dict :
        A dictionary with the current date; the exchange rate as float, and the source
        of the data (BCV).
    """
    url = "http://www.bcv.org.ve/"

    #Create the default information
    data_output = {
        #"date": date.today().strftime("%d/%m/%Y "),  # Current date
        "date":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "exchange_rate": np.nan,
        "exchange": "Bs./$",
        "source": "BCV",
    }
    # When a error is raise when loading the page, return a Nan in the exchange Rate
    try:
        html = urlopen(url)  # Url of the Central Bank of Venezuela
    except HTTPError as e:
        print("HTTPError")
        print("The Exception raised was:")
        print(e)
        return data_output 
    except URLError as e:
        print("The server could not be found!")
        return data_output
    except Exception as e:
        print(f"Something unexpected happen trying opening {url}")
        print("The Exception raised was:")
        print(e)
        return data_output
    else:

        # Scrap the exchange Rate of $ to BS
        bs = BeautifulSoup(html.read(), "html.parser")
        dollar_boc = bs.find(id="dolar").find(
            "div", {"class": "col-sm-6 col-xs-6 centrado"}
        )

        # Convert the exchange rate text to a float
        dollar_text = dollar_boc.get_text().replace(".", "").replace(",", ".")
        exchange_rate = float(dollar_text)
        assert isinstance(exchange_rate,float),"exchange_rate must be float"

        # Update exchange rate dictionary
        data_output.update({"exchange_rate": exchange_rate})
        assert isinstance(data_output,dict), "data_output must be a dict object"
    return data_output


def gama_product_search(product: str) -> pd.DataFrame:
    """
    Scrape the search results from the Gama supermarket website.

    Parameters
    ----------
    product : str
        The name of the product to look for.

    Returns
    -------
    pd.DataFrame :
        a DataFrame with information of the product. It has columns for the name
        the price, availability, date, the store name, and the search_term.

    """

    #Prepare product name for the url search
    product_cl = product.strip()  # Strip white spaces
    product = re.sub(
        "\s", "+", product_cl
    )  # Replace white spaces with plus marker, to make the search valid

    store_name = "Gama"
    url = (
        "https://gamaenlinea.com/search/?text=" + product
    )  # Url to get the search page of the product

    print("-" * 20)
    print(f"Searching {product_cl} in {store_name} Supermarket WegPage")
    print("Trying url  : " + url)

    # Check for HTTP and URL errors
    try:
        html = urlopen(url)  # Get the hmtl code
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print("The server could not be found!")
        return None
    except Exception as e:
        print(f"Something unexpected happen trying opening {url}")
        print("The Exception raised was:")
        print(e)
        print(" None will be return")
        return None
    else:
        bs = BeautifulSoup(
            html.read(), "html.parser"
        )  # BeatifulSoup Object to parse the html
        # products_list = bs.find_all("li",class_="product__list--item")#This class is the one that will let us search if element list
        products_information = []  # List to save all the products information
        products_information = products_information + gama_get_products(
            bs
        )  # Get the search result of the first search page

        link_list = [url]  # List of link opened

        # Open every page result and get the list of products on it
        if bs.find("ul", class_="pagination") != None:
            for page_ref in bs.find("ul", class_="pagination").find_all("a"):
                url = (
                    "https://gamaenlinea.com" + page_ref["href"]
                )  # Link to the new page result

                # Check if the new link was not already open
                if url not in link_list:
                    link_list.append(url)  # Update list of link already open
                    # Check for HTTP and URL errors
                    try:
                        html = urlopen(url)  # Get the hmtl code
                    except HTTPError as e:
                        print(e)
                    except URLError as e:
                        print("The server could not be found!")
                    else:
                        bs = BeautifulSoup(
                            html.read(), "html.parser"
                        )  # BeatifulSoup Object to parse the html d
                        new_gama_products = gama_get_products(bs)
                        assert isinstance(
                            new_gama_products, list
                        ), f"The function gama_get_products() was unavailable to make a product list from thi url: {url}"
                        
                        # Add the products of the new page
                        products_information = (
                            products_information + new_gama_products
                        )  

        # Convert data to DataFrame format
        df_data = pd.DataFrame(
            products_information,
            columns=["product_name", "product_price", "product_availability"],
        )  
        add_general_columns(df_data, store_name, product_cl)
        assert df_data.shape[1] == 6, f"The DataFrame has extra columns"

        return df_data


def central_m_product_search(product: str) -> pd.DataFrame:
    """
    Scrape the search results from the Central  Madeirense   supermarket website.

    Parameters
    ----------
    product : str
        The name of the product to look up.

    Returns
    -------
    df_data : pd.DataFrame
        a DataFrame with information of the product. It has columns for the name
        the price, availability, date, the store name, and the search_term.
    """
    store_name = "Central Madeirense"

    product_cl = product.strip()  # Strip white spaces
    product = re.sub(
        "\s", "+", product_cl
    )  # Replace white spaces with plus marker, to add it to the url link

    url = f"https://tucentralonline.com/La-Lagunita-44/?count=40&paged=&post_type=product&s={product}&asp_active=1&p_asid=1&p_asp_data=1&current_page_id=143&woo_currency=BSD&qtranslate_lang=0&filters_changed=0&filters_initial=1&asp_gen%5B%5D=title&asp_gen%5B%5D=content&asp_gen%5B%5D=excerpt&customset%5B%5D=product&customset%5B%5D=postt"  # Url to get the search page of the product

    print("\n" + "-" * 20)
    print(f"Searching {product_cl} in {store_name} Supermarket WegPage")

    # Check for HTTP and URL errors before opening the search result page
    try:
        html = urlopen(url)  # Get the hmtl code
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print("The server could not be found!")
        return None
    except Exception as e:
        print(f"Something unexpected happen trying opening {url}")
        print("The Exception raised was:")
        print(e)
        print(" None will be return")
        return None
    else:
        bs = BeautifulSoup(
            html.read(), "html.parser"
        )  # BeatifulSoup Object to parse the html

        products_information = []  # List to save all the products information
        print("-------------")
        print(f"Trying Page 1 of {store_name} search results")
        products_information.append(
            central_m_get_product(url)
        )  # Get the search result of the first search page

        link_list = [url]  # List of link opened

        # , if there are more than one result pages, Get tej data of all of them
        if len(bs.find_all("a", class_="page-numbers")) > 0:
            num_pages = bs.find_all("a", class_="page-numbers")[
                -2
            ].get_text()  # Ge the number search result pages

            # Creates links for every page result, after the first one and append it to the link list
            for num in range(2, int(num_pages) + 1):
                new_link = bs.find("a", class_="page-numbers")["href"].replace(
                    r"page/2/", r"page/" + str(num) + r"/"
                )
                link_list.append(new_link)

            # Open every page result and get the list of products on it
            for pagination, page_ref in enumerate(link_list, start=2):
                print("-------------")
                print(f"Trying Page {pagination} of {store_name} search results")
                products_information.append(central_m_get_product(page_ref))

        df_data = pd.concat(products_information)
        df_data = add_general_columns(df_data, store_name, product_cl)
        assert df_data.shape[1] == 6, f"The DataFrame has extra columns"
        return df_data


def plazas_product_search(product: str) -> pd.DataFrame:
    """
    Scrape the search results from the Plazas   supermarket website.

    Parameters
    ----------
    product : str
        The name of the product to look up.

    Returns
    -------
    df_data : pd.DataFrame
        a DataFrame with information of the product. It has columns for the name
        the price, availability, date, the store name, and the search_term.
    """
    # Clean and prep the search term
    product_cl = product.strip()  # Strip white spaces
    product = re.sub(
        "\s", "%20", product_cl
    )  # Replace white spaces with plus marker, to make the search in the url

    store_name = "Plazas"

    url = (
        "https://www.elplazas.com/Products.php?des=" + product
    )  # Url to get the search page of the product
    print("\n" + "-" * 20)
    print(f"Searching {product_cl} in {store_name} Supermarket WegPage")

    # Collect raw data from the page result
    products_data = collect_data_global(
        url, "div", "Product", "div", "Description", "div", "Price"
    )

    # If the raw data is not empty, clean it
    if not products_data.empty:
        print(f"Prepping Data from {store_name} supermarket")

        products_data["product_name"] = products_data[
            "product_name"
        ].str.strip()  # Cleans name text

        def clean_price(price_text: str, currency="Bs.") -> str:
            """Cleans the price text of Plazas supermarket"""
            if "IVA" in price_text:
                price_text = price_text.split("IVA")[1]

            price_text = re.sub("\s", "", price_text)
            price_text = price_text.replace("(E)", "").replace(
                ",", ""
            )  # Clean price Tag text
            price_text = currency + " " + price_text  # Use the corresponding currency
            return price_text

        products_data["product_price"] = products_data["product_price"].apply(
            clean_price
        )  # Cleans price text

        print(f"Data From {store_name} supermarket ready")
        add_general_columns(
            products_data, store_name, product_cl
        )  # Adds date, store name and search term
        assert products_data.shape[1] == 6, f"The DataFrame has extra columns"
        return products_data
    else:
        return None


def plansuarez_product_search(product: str) -> pd.DataFrame:
    """
    Scrape the search results from the Plansuarez   supermarket website.

    Parameters
    ----------
    product : str
        The name of the product to look up.

    Returns
    -------
    df_data : pd.DataFrame
        a DataFrame with information of the product. It has columns for the name
        the price, availability, date, the store name, and the search_term.
    """

    # Clean and prepare search term
    product_cl = product.strip()  # Strip white spaces
    product = re.sub(
        "\s", "%20", product_cl
    )  # Replace white spaces with plus marker, to make the search valid in the url

    store_name = "Plan Suarez"

    url = f"https://www.plansuarez.com/index.php?route=product/search&search={product}&limit=100"  # Url of the search result page

    print("\n" + "-" * 20)
    print(f"Searching {product_cl} in {store_name} Supermarket WegPage")

    # Get Raw data from the page result
    products_data = collect_data_global(
        url, "div", "product-thumb", "div", "name", "span", "price-normal"
    )

    # if the data frame is not empty, clean it
    if not products_data.empty:
        print(f"Cleaning Data from {store_name} supermarket")
        products_data["product_name"] = products_data[
            "product_name"
        ].str.strip()  # Clean the name

        products_data["product_price"] = (
            products_data["product_price"]
            .replace("Bs.", "Bs. ", regex=True)
            .replace(",", "", regex=True)
        )  # Clean the price text

        print(f"Data From {store_name} supermarket ready")
        add_general_columns(products_data, store_name, product_cl)
        assert products_data.shape[1] == 6, f"The DataFrame has extra columns"
        return products_data
    else:
        return None


def scrape_raw_data(products: list) -> pd.DataFrame:
    """
    Scrape product information from Plaza, Gama, Central Madeirense, and Plan Suarez.

    Parameters
    ----------
    products : list
        A list of product to search for.

    Returns
    -------
    raw_data : pd.DataFrame
        A Pandas Data Frame with the following columns product_name, product_price,
        product_availability, date, store,and search_term.
    """
    data_list = []
    for product in products:
        product = product.lower()

        data_list.append(plazas_product_search(product))
        data_list.append(gama_product_search(product))
        data_list.append(central_m_product_search(product))
        data_list.append(plansuarez_product_search(product))
        time.sleep(3)

    # Check if all the data is empty
    if not all(i is None for i in data_list):

        raw_data = pd.concat(data_list).reset_index(drop=True)
        assert raw_data.shape[1] == 6, f"The DataFrame has extra columns"
        print("Raw data extracted")
        return raw_data
    else:
        return pd.DataFrame(
            columns=[
                "product_name",
                "product_price",
                "product_availability",
                "date",
                "store",
                "search_term",
            ]
        )


def scrape_prep_data(products: list, exchange_rate=None) -> pd.DataFrame:
    """
    Add a column to show all the prices in us dollars and drop unrelated rows.

    Parameters
    ----------
    products : list
        a list of strings that will be search on all the supermarkets

    exchange_rate : float
        (optional) a float number representing the exchange rate ($/Bs).
        If no value is given, the exchange rate will be scrape from the BCV web page.
    Return
    ----------
    pd.DataFrame :
        It's a Pandas DataFrame of the raw data scrape from the supermarkets web pages
        with out unrelated products and a new column with the price in USA Dollars of
        the product.
    """
    raw_data = scrape_raw_data(products)  # Get the raw data
    assert raw_data.shape[1] == 6, f"The DataFrame has extra columns"
    if raw_data.shape[0] != 0:
        # If the product is a single, check if the name of the product contains it
        search_terms = list(raw_data["search_term"].unique())
        for search_term in search_terms:
            if not " " in search_term.strip():
                print(f"{search_term}")
                condition = raw_data.loc[
                    raw_data["search_term"] == search_term.lower().strip(),
                    "product_name",
                ].str.contains(search_term.strip(), case=False)

                raw_data = raw_data.drop(
                    raw_data.loc[
                        raw_data["search_term"] == search_term.lower().strip(), :
                    ][~condition].index
                )
                raw_data = raw_data.reset_index(drop=True)

        # If No exchange rate is given, scrape the current exchange rate according to the BCV
        if exchange_rate == None:
            rate_bs_dollar = bcv_exchange_rate()["exchange_rate"]
        else:
            rate_bs_dollar = exchange_rate

        def convert_bs_dollar(price_text: str, rate_bs_dollar: float) -> float:
            """Converts Bs to US Dollars using the given exchange rate (Bs.s/$), dollar prices are ignore"""

            if "Bs." in price_text:
                price = float(price_text.replace("Bs.", "").strip())
                price = round(price / rate_bs_dollar,2)
                return price
            elif "$" in price_text:
                price = float(price_text.replace("$", "").strip())
                return price

        # Make a column for prices in dollars,
        raw_data["product_price_dollar"] = raw_data["product_price"]
        raw_data["product_price_dollar"] = (
            raw_data["product_price_dollar"]
            .apply(lambda x: convert_bs_dollar(x, rate_bs_dollar))
            .astype("float")
        )

        process_data = raw_data.reset_index(drop=True)
        assert raw_data.shape[1] == 7, f"The DataFrame has extra columns"
        return process_data
    else:
        print("No Data was found for the list of products.")