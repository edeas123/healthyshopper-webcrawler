# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:07:52 2017

@author: oodiete
"""

from bs4 import BeautifulSoup
import requests

base_url = "https://www.realcanadiansuperstore.ca"
section = "Food"
categories = [{"name": "Fruits&Vegetables", "ref": "RCSS001001000000"}]#,
#              "https://www.realcanadiansuperstore.ca/Food/Deli-%26-Ready-Meals/c/RCSS001002000000",
#              "https://www.realcanadiansuperstore.ca/Food/Bakery/c/RCSS001003000000",
#              "https://www.realcanadiansuperstore.ca/Food/Meat-%26-Seafood/c/RCSS001004000000",
#              "https://www.realcanadiansuperstore.ca/Food/Dairy-and-Eggs/c/RCSS001005000000",
#              "https://www.realcanadiansuperstore.ca/Food/Drinks/c/RCSS001006000000",
#              "https://www.realcanadiansuperstore.ca/Food/Frozen/c/RCSS001007000000",
#              "https://www.realcanadiansuperstore.ca/Food/Pantry/c/RCSS001008000000",
#              "https://www.realcanadiansuperstore.ca/Food/Natural-%26-Organic/c/RCSS001009000000"]

def request_page(url):
    """Util function to request pages"""
    
    r = requests.get(url)
    if r.status_code !=  200:
        print "{0}: {1}".format(r.status_code, r.reason)
        return None

    return r.text


for category in categories:
    
    # get url
    url = "{}/{}/{}/{}/{}".format(base_url, section, category["name"], "c", category["ref"])
    
    # retrieve page
    page = request_page(url)
    
    # pull data from page
    soup = BeautifulSoup(page, "lxml")
    
    # parse page
    subcategory_divs = soup.find_all("div", {"class": "wrapper-subcategory"})
    for subcategory_div in subcategory_divs:
        
        # get url
        url = "{}/{}/{}{}".format(base_url, section, category["name"], subcategory_div["data-ajax-url"])

        # retrieve page
        page = request_page(url)

        # pull data from page
        soup = BeautifulSoup(page, "lxml")

        # parse page
        product_divs = soup.find_all("div", {"class": "product-name-wrapper"})
        for product_div in product_divs:
            
            # get url
            url = "{}{}".format(base_url, product_div.a["href"])
    
            # retrieve page
            page = request_page(url)
    
            # pull data from page
            soup = BeautifulSoup(page, "lxml")            
            
            # parse page
            nutrition_labels = soup.find_all("div", {"class": "nutrition-summary-label"})
            nutrition_values = soup.find_all("div", {"class": "nutrition-summary-value"})
            nutrition = {}
            
            for i in range(len(nutrition_labels)):
                nutrition[nutrition_labels[i].text.strip("\n\t")] = nutrition_values[i]
