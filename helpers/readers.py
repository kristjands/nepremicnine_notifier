import requests
import concurrent.futures
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from helpers.listings import Listings
from helpers.page import Page


class Readers:
    def __init__(self, page_config: Page, listings: Listings):
        self.page_config = page_config
        self.listings = listings

    def read(self):
        if self.page_config.type == 'scroll':
            self.read_scroll()
        else:
            self.read_pages()

    def read_pages(self):
        for i in range(1, 5000):
            page = requests.get(self.page_config.get_serach_url(i))
            soup = BeautifulSoup(page.content, 'html.parser')

            self.parse_ads(soup)
    
    def read_scroll(self):
        driver = webdriver.Chrome('./chromedriver.exe') # TODO
        driver.get(self.page_config.page_url)

        time.sleep(self.page_config.wait_load_seconds)

        try:
            js_func = '''function scrollToBottom() {{
                prev = document.getElementsByClassName("{scroll_element}")[0].scrollTop; 
                    document.getElementsByClassName("{scroll_element}")[0].scrollTop += document.getElementsByClassName("{scroll_element}")[0].scrollHeight; 
                    setTimeout(function() {{ 
                        if (document.getElementsByClassName("{scroll_element}")[0].scrollTop != prev) {{ 
                            scrollToBottom(); 
                        }} 
                        else {{ 
                            document.getElementsByTagName("body")[0] += \'<div id="scriptFunctionDoneScrollingToBottom">scriptFunctionDoneScrollingToBottom</div>\'; 
                        }} 
                    }}, 3000); 
                }}; 
                scrollToBottom();'''.format(scroll_element=self.page_config.scroll_element)

            driver.execute_script(js_func)

            wait = WebDriverWait(driver, self.page_config.timeout_for_scroll_seconds)
            wait.until(ec.visibility_of_element_located((By.ID, 'scriptFunctionDoneScrollingToBottom')))

            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            
            self.parse_ads(soup)

        finally:
            driver.quit()
        
    def parse_ads(self, soup: BeautifulSoup):
        ads = soup.find_all(self.page_config.bs4_block, attrs=self.page_config.bs4_attrs)
        ads_len = len(ads)

        with concurrent.futures.ThreadPoolExecutor(max_workers=ads_len) as executor:
            for ad in ads:
                executor.submit(self.listings.parse_listing, ad, self.page_config)
