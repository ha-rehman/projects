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
        main_page = driver.current_window_handle  # Store the parent_window_handle for future use
        confedantials_images = []
        for my_href in my_hrefs:
            # opening new window and switch driver
            try:
                driver.execute_script("window.open('" + str(my_href) + "');")
                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # Induce WebDriverWait for the number_of_windows_to_be 2
                windows_after = driver.window_handles
                product_page = [x for x in windows_after if x != main_page][0]  # Identify the newly opened window
                driver.switch_to.window(product_page)  # switch_to the new window
                time.sleep(3)  # perform your webscraping here
                print(product_page)  # print the page title or your perform your webscraping

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
                    driver.switch_to.window(lens_page)
                    time.sleep(3)

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'FttNLb')))
                    products = driver.find_element(By.CLASS_NAME, 'FttNLb')
                    print(products)

                    # imgs = [elements.get_attribute('data-thumbnail-url') for elements in products.find_elements(By.CLASS_NAME, 'jFVN1')]
                    # texts = driver.get_elements(By.CLASS_NAME, 'o9C2v')
                    #
                    # for txt in texts:
                    #     print(txt)


                    print("inner closed")
                    driver.close()
                    driver.switch_to.window(product_page)
                except:
                    driver.close()
                    driver.switch_to.window(product_page)
                    confedantials_images.append(my_href)
                    pass

                print("outer closed")
                driver.close()  # close the window
                driver.switch_to.window(main_page)  # switch_to the parent_window_handle
            except:
                print("Outer Exception")
                driver.close()  # close the window
                driver.switch_to.window(main_page)  # switch_to the parent_window_handle

                pass
        driver.quit()  # quit your program

        urllib.urlretrieve(imgs, "captcha.png")

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


