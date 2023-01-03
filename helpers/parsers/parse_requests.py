import requests
import concurrent.futures
from bs4 import BeautifulSoup

from ..page import Page
from ..listings import Listings

def parse(page_config: Page, listings: Listings) -> None:
    for i in range(1, 1000):
        page = requests.get(page_config.get_serach_url(i))
        soup = BeautifulSoup(page.content, 'html.parser')

        ads = soup.find_all(page_config.bs4_block, attrs=page_config.bs4_attrs)
        ads_len = len(ads)
        if ads_len == 0:
            break

        with concurrent.futures.ThreadPoolExecutor(max_workers=ads_len) as executor:
            for ad in ads:
                executor.submit(listings.parse_listing, ad, page_config)
