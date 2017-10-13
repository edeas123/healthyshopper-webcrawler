# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 12:20:24 2017

@author: oodiete
"""

import scrapy

class FoodSpider(scrapy.Spider):
    name = "food"
    base_url = "https://www.realcanadiansuperstore.ca"
    section = "Food"    

    def start_requests(self):
        """ start requests from defined urls"""
        

        categories = [{"name": "Fruits&Vegetables", "ref": "RCSS001001000000"},
                      {"name": "Deli-%26-Ready-Meals", "ref": "RCSS001002000000"},
                      {"name": "Bakery", "ref": "RCSS001003000000"},
                      {"name": "Meat-%26-Seafood", "ref": "RCSS001004000000"},
                      {"name": "Dairy-and-Eggs", "ref": "RCSS001005000000"},
                      {"name": "Drinks", "ref": "RCSS001006000000"},
                      {"name": "Frozen", "ref": "RCSS001007000000"},
                      {"name": "Pantry", "ref": "RCSS001008000000"},
                      {"name": "Natural-%26-Organic", "ref": "RCSS001009000000"}]
        
        for category in categories:
            
            # get url
            url = "{}/{}/{}/{}/{}".format(self.base_url, self.section, category["name"], "c", category["ref"])
            yield scrapy.Request(url=url, callback=self.parse, meta=category)
            
    
    def parse(self, response):
        
        subpaths = response.xpath("//div[@class='wrapper-subcategory']/@data-ajax-url").extract()
        for subpath in subpaths:
            url = "{}/{}/{}{}".format(self.base_url, self.section, response.meta["name"], subpath)
            request = response.follow(url, self.parse_sub)
            
            yield request
            
    def parse_sub(self, response):
        
        subpaths = response.xpath("//div[@class='product-name-wrapper']/a/@href").extract()
        for subpath in subpaths:
            url = "{}{}".format(self.base_url, subpath)
            request = response.follow(url, self.parse_product)
            
            yield request
            
    def parse_product(self, response):
        
        product = {}
        nutrition = {}
        nutrition_labels = response.xpath("//span[@class='nutrition-summary-label']/text()").extract()
        nutrition_values = response.xpath("//span[@class='nutrition-summary-value']/text()").extract()
        
        for i in range(len(nutrition_labels)):
            label = nutrition_labels[i].strip("();\n\t")
            value = nutrition_values[i].strip("();\n\t")
            nutrition[label] = value
            
        main_nutrition = response.xpath("//div[@class='row-nutrition-fact-attr hidden-sm row']//div[@class='main-nutrition-attr first']")
        for main_n in main_nutrition:
            label = main_n.xpath("span[@class='nutrition-label']/text()").extract_first().strip("();\n\t")
            value = main_n.xpath("text()").extract()[1].strip("();\n\t")
            percent = main_n.xpath("span[@class='dv']/text()").extract_first(default="NA")
            nutrition[label] = {"value": value, "percent": percent}
            
        sub_nutrition = response.xpath("//div[@class='row-nutrition-fact-attr hidden-sm row']//div[@class='sub-nutrition-attr first']")
        for sub_n in sub_nutrition:
            label = sub_n.xpath("span[@class='nutrition-label']/text()").extract_first().strip("();\n\t")
            value = sub_n.xpath("text()").extract()[1].strip("();\n\t")
            percent = sub_n.xpath("span[@class='dv']/text()").extract_first(default="NA")
            nutrition[label] = {"value": value, "percent": percent}
            
        price = response.xpath("//div[@class='module-product-info']/@data-product-price").extract_first()
        product_name = response.xpath("//div[@class='module-product-info']//h1[@class='product-name']/text()").extract()[1].strip("();\n\t")
        category = response.xpath("//div[@class='module-filter-and-sort container hidden-sm']//li[@class='item']/a/text()").extract()
        category_last = response.xpath("//div[@class='module-filter-and-sort container hidden-sm']//li[@class='item last']/a/text()").extract()
        category.extend(category_last)
        
        product["price"] = price
        product["name"] = product_name
        product["nutrition"] = nutrition
        product["categories"] = category
        
        yield product
        

