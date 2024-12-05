import time

import requests
import docx
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
import argparse


def scrapping(csv_file, data_directory):

    DRIVER_PATH = './chromedriver.exe'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')


    # perform pre-processing steps
    print("Column Names: ", csv_file.columns.values)
    urls = csv_file['URL'].tolist()
    names = csv_file['Name'].tolist()
    counter = 1

    for name, url in zip(names,urls):
        print("Scrapping of Document ", counter, ".....")
        print("Document Name: ", name)
        print("Document URL: ", url)

        # scrap document
        driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
        driver.get(url)
        truncate_data(driver)
        content = driver.find_element_by_id('mw-content-text')

        # write document
        fname = data_directory + name + ".docx"
        # with open(fname, "w", encoding="utf-8") as f:
        #     f.write(content.text)

        mydoc = docx.Document()
        mydoc.add_paragraph(content.text)
        mydoc.save(fname)

        print("Document", counter, "scraped successfully and saved at ", fname)
        print("")
        counter += 1


def truncate_data(driver):

    try:
        element = driver.find_element_by_xpath("//table[@role='presentation']")
        driver.execute_script(""" 
                         var element = arguments[0];
                         element.parentNode.removeChild(element);
                         """, element)
    except :
        pass

    try:
        element = driver.find_element_by_class_name("infobox")
        driver.execute_script("""
                         var element = arguments[0];
                         element.parentNode.removeChild(element);
                         """, element)
    except :
        pass



    try:
        content = driver.find_elements_by_class_name('thumb')
        for element in content:
            driver.execute_script("""
                       var element = arguments[0];
                       element.parentNode.removeChild(element);
                       """, element)
    except :
        pass

    try:
        extarnal_link = driver.find_element_by_id('References')
        element = extarnal_link.find_element_by_xpath('..')
        driver.execute_script("""
                   var element = arguments[0];
                   element.parentNode.removeChild(element);
                   """, element)
    except:
        pass

    try:
        element = driver.find_element_by_class_name('reflist')
        content = element.find_elements_by_xpath("following-sibling::*")

        driver.execute_script("""
                           var element = arguments[0];
                           element.parentNode.removeChild(element);
                           """, element)

        for element in content:
            driver.execute_script("""
                       var element = arguments[0];
                       element.parentNode.removeChild(element);
                       """, element)

    except:
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str)
    parser.add_argument('--category', type=str)
    args = parser.parse_args()

    csv_path = 'data/' + args.csv
    data_directory = "data/%s/" %(args.category)
    csv_file = pd.read_csv(csv_path, encoding= 'unicode_escape')

    scrapping(csv_file, data_directory)


