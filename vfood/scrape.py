# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:57:22 2021

@author: Julio

This module is for scarping the DataFrom  the Websites of the SupperMarkets

"""

# Web Scraping libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError  # For error handling
from urllib.error import URLError  # For error handling

# Data manipulation libraries
import pandas as pd


def collect_data_global(
    url: str,
    list_type: str,
    list_class: str,
    name_type: str,
    name_class: str,
    price_type: str,
    price_class: str,
) -> pd.DataFrame:
    """
    Collect product information on the website

    Parameters
    ----------
    url : str
        Url link of the website.

    list_type : str
        The html tag, of the parent element that list all the product information.

    list_class : str
        The name of the class that lists all the products.

    name_type : str
        Html tag name that has the name of the product.

    name_class : str
        Html class name that has the name of the product.

    price_type : str
        Html tag name that has the price of the product.

    price_class : str
        Html class name that has the price of the product.

    Returns
    ----------
    df_data : pd.DataFrame
        A DataFrame with the columns: product_name, product_price, and product_availability. If the search page result was no information, a empty Data Frame will be return.

    """

    print("Trying url  : " + url)

    # Create a empty Data Frame with the main columns
    df_data = pd.DataFrame(
        columns=["product_name", "product_price", "product_availability"]
    )
    # Check for HTTP and URL errors
    try:
        html = urlopen(url)  # Get the hmtl code
    except HTTPError as e:
        print(e)
        return df_data
    except URLError as e:
        print("The server could not be found!")
        return df_data
    except Exception as e:
        print(f"Something unexpected happen trying opening {url}")
        print("The Exception raised was:")
        print(e)
        print(" None will be return")
        return df_data
    else:
        print("Html Loaded successfully from " + url)
        bs = BeautifulSoup(html.read(), "html.parser")

        products_list = bs.find_all(
            list_type, class_=list_class
        )  # List of all the products in the url
        products_information = []  # Products information list
        for x, product_box in enumerate(products_list):
            print(f"Product {x} of this page")
            raw_text = product_box.find(name_type, class_=name_class)
            raw_price = product_box.find(price_type, class_=price_class)
            # If the price and text is found, ge the raw text
            if raw_text != None and raw_price != None:
                product_name = raw_text.get_text()  # Gets  the product Name

                product_price = raw_price.get_text()  # Gets the product price tag text

                availability = (
                    True  # For pages where availability does not have a marker
                )

                products_information.append(
                    [product_name, product_price, availability]
                )  # Adds info to the products list

        print(f"All available data from {url} collected")

        # If information was collected make it presentable, else pass a empty DataFrame.
        if len(products_information) > 0:
            print(f"{len(products_information)} products collected from {url} ")
            df_data = pd.DataFrame(
                products_information,
                columns=["product_name", "product_price", "product_availability"],
            )  # Convert data to DataFrame format
            return df_data
        else:
            print(f"0 Products where safe from {url}")
            return df_data


def gama_get_products(bs) -> list:
    """
    Get all the product listed in the Gama supermarket page result

    Parameters
    ----------
    bs : BeautifulSoup
        Gama supermarket website result page

    Returns
    -------
    list : list
        A list with columns for the product name, its price, and availability at the moment of the search, for all the product in the page pass
    """
    currency = "$"  # The currency use in the Web Page

    products_list = bs.find_all(
        "li", class_="product__list--item"
    )  # This class is the one that will let us search if element list
    products_information = []  # List to save all the products information
    for product_box in products_list:
        product_name = product_box.find(
            "a", class_="product__list--name"
        ).get_text()  # Gets  the product Name

        product_price = product_box.find(
            "div", class_="from-price-value"
        ).get_text()  # Gets the product price tag text
        product_price = (
            product_price.replace("Total Ref. ", "").replace(".", "").replace(",", ".")
        )  # Clean price Tag text
        product_price = currency + " " + product_price  # Use the correponing currency

        # Try to find if the button used is the one that shows availability and update the variable
        availability_button = product_box.find(
            "button",
            class_="btn btn-primary btn-block glyphicon glyphicon-shopping-cart js-enable-btn ec-add-cart-btn",
        )
        if availability_button != None:
            availability = True
        else:
            availability = False

        products_information.append(
            [product_name, product_price, availability]
        )  # Safe product information in main list

        # print(product_name + " : " +product_price +" Availability: " + str(availability))

    return products_information


def central_m_get_product(url) -> pd.DataFrame:
    """
    Get all the products listed in the Central Madeirense supermarket page result

    Parameters
    ----------
    url : str
        The url of central Madeirense supermarket page result

    Returns
    -------
    page_data
        A Pandas DataFrame with the following columns product_name,	product_price, product_availability, date, store, and	search_term

    """

    page_data = collect_data_global(
        url, "div", "product-inner", "div", "description", "span", "price"
    )  # Get raw data

    # If the DataFrame is not empty, clean the price and name of the product
    if not page_data.empty:
        print("Cleaning Data from Central Madeirense")
        page_data["product_name"] = page_data[
            "product_name"
        ].str.strip()  # Cleans the name

        def price_clean(price_text):
            """Function to clean price text of Central Madeirense supermarket web page"""
            price_text = (
                price_text.replace("\xa0", "")
                .replace(".", "")
                .replace(",", ".")
                .replace("#", "")
                .strip()
            )
            if " " in price_text:
                price_text = price_text.split(" ")[1]
            price_text = "$ " + price_text
            return price_text

        page_data["product_price"] = page_data["product_price"].apply(
            price_clean
        )  # Cleans the price

    return page_data
