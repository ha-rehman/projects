import os
import re
import urllib

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
from price_parser import Price
import urllib
import pandas as pd


class TableScraper:

    def fetch(self, url):
        # Driver will install
        options = Options()
        options.add_argument("user-data-dir=C:\\Users\\abdul\\AppData\\Local\\Google\\Chrome\\User Data")
        # options.add_argument('disable-extensions')
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
        # driver.maximize_window()
        # driver.implicitly_wait(200)
        # delay so that page proper load
        delay = 50
        try:
            # wait function unti
            # l 'secDig' will show on page
            # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'secDig')))
            driver.implicitly_wait(10)

        except TimeoutException:
            print("Loading took too much time!")
        return driver

    def parse(self, driver):
        my_hrefs = [my_elem.get_attribute("href") for my_elem in
                    driver.find_element(By.CLASS_NAME, "results-base").find_elements(By.TAG_NAME, "a")]
        product_imgs = [my_elem.get_attribute("src") for my_elem in
                    driver.find_element(By.CLASS_NAME, "results-base").find_elements(By.TAG_NAME, "img")]
        main_page = driver.current_window_handle  # Store the parent_window_handle for future use
        confedantials_images = []
        data_matrix = []
        original_image_index = 1
        os.mkdir(os.path.join("visual", str(original_image_index)))

        try:
            for my_href, product_img in zip(my_hrefs, product_imgs):
                index_flag = False
                # opening new window and switch driver
                try:
                    inner_flag = False
                    outer_flag = False
                    driver.execute_script("window.open('" + str(my_href) + "');")
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # Induce WebDriverWait for the number_of_windows_to_be 2
                    windows_after = driver.window_handles
                    product_page = [x for x in windows_after if x != main_page][0]  # Identify the newly opened window
                    driver.switch_to.window(product_page)  # switch_to the new window
                    time.sleep(3)  # perform your webscraping here
                    # print(product_page)  # print the page title or your perform your webscraping
                    outer_flag = True
                    # open popup
                    first_image = driver.find_element(By.CLASS_NAME, "image-grid-col50")
                    first_image.click()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'desktop-image-zoom-primary-image')))
                    time.sleep(2)
                    popup_image = driver.find_element(By.CLASS_NAME, 'desktop-image-zoom-primary-image')

                    # right click and select from options
                    actionChains = ActionChains(driver)
                    actionChains.context_click(popup_image).perform()
                    time.sleep(2)

                    pyautogui.press('down', presses=6)
                    time.sleep(3)
                    pyautogui.press('enter')

                    # switch to new window
                    try:
                        page_after = driver.window_handles
                        lens_page = [x for x in page_after if x != main_page and x != product_page][0]
                        time.sleep(5)
                        driver.switch_to.window(lens_page)
                        inner_flag = True
                        time.sleep(10)

                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, 'FttNLb')))

                        # see_more = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe')
                        # see_more.click()
                        # products = driver.find_element(By.CLASS_NAME, 'FttNLb')
                        # print(products)

                        imgs = [my_elem.get_attribute("data-thumbnail-url") for my_elem in
                         driver.find_element(By.CLASS_NAME, "aah4tc").find_elements(By.CLASS_NAME, 'jFVN1')]

                        imgs_links = [my_elem.get_attribute("data-action") for my_elem in
                                driver.find_element(By.CLASS_NAME, "aah4tc").find_elements(By.CLASS_NAME, 'jFVN1')]

                        texts = [my_elem.text for my_elem in
                                driver.find_element(By.CLASS_NAME, "aah4tc").find_elements(By.CLASS_NAME, 'o9C2v')]

                        visual_image_index = 1

                        for img, img_link, text in zip(imgs, imgs_links, texts):
                            if Price.fromstring(text).currency == "₹":
                                text_split = text.split("•")
                                price_tag = text_split[0].strip()
                                price = price_tag.split("₹")[-1]
                                source_link = text_split[1]

                                urllib.request.urlretrieve(img, os.path.join("visual", str(original_image_index), str(visual_image_index)+'.png'))

                                index_flag = True
                                row_list = [original_image_index, visual_image_index, price, img_link]
                                visual_image_index += 1
                                data_matrix.append(row_list)

                    except:
                        print("inner exception")
                        confedantials_images.append(my_href)
                        pass

                    finally:

                        if index_flag:
                            urllib.request.urlretrieve(product_img, os.path.join("visual", str(original_image_index), "original.png"))
                            original_image_index += 1
                            os.mkdir(os.path.join("visual", str(original_image_index)))

                        if inner_flag:
                            driver.close()
                            driver.switch_to.window(product_page)

                except:
                    print("outer exception")
                    pass
                finally:
                    if outer_flag:
                        driver.close()  # close the window
                        driver.switch_to.window(main_page)  # switch_to the parent_window_handle
        except Exception as e:
            print(e)
            pass
        finally:
            driver.quit()  # quit your program
            print(data_matrix)
            df = pd.DataFrame(data_matrix, columns=['original Image Index', 'Visual ID', 'Price', 'Link'])
            df.to_csv('Scrapped_data.csv', index=False)

        # # solution 2
        # pr

        # oducts = driver.find_elements(By.CLASS_NAME, "product-base")
        # for product in products:
        #     product.click()
        #     driver.find_elements(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        #     driver.get()




            # solution 1
        # soup = BeautifulSoup(html.page_source, "html.parser")
        # products = soup.findAll(class_="product-base")
        #
        # for product in products:
        #     links = product.find_all("a")
        #     for link in links:
        #         print(link['href'])
        #         print("========================")


        # soup = BeautifulSoup(html.page_source, "html.parser")
        # Tables = soup.findAll(class_="tablaActProIn")
        # # extract each table from tables
        # for Table in Tables:
        #     # library for display data in tables
        #     table = PrettyTable()
        #     rows = Table.findAll('tr')
        #     for row in rows:
        #         cols = row.findAll("td")
        #         columns = []
        #         if len(cols) == 0:
        #             cols = row.findAll("th")
        #         for index in range(len(cols)):
        #             # print(cols[index].text)  # prints text from the element
        #             text = str(cols[index].text)
        #             text = text.replace('\n', '')  # for removing new line format specifier
        #             columns.append(text)
        #         # equalizing columns length for pretty table
        #         if len(columns) <= 1:
        #             columns.insert(0, "")
        #             columns.append("")
        #         table.add_row(columns)
        #     # output of each table
        #     print(table)

    def to_csv(self):
        pass

    def run(self):
        response = self.fetch('https://www.myntra.com/men-tshirts')
        self.parse(response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper = TableScraper()
    scraper.run()


