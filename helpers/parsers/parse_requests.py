import requests
import concurrent.futures
from bs4 import BeautifulSoup, element
from typing import Tuple

from helpers.page import PageRequest
from helpers.listing import Listing

def parse(page_config: PageRequest, listings) -> None:
    for i in range(1, 1000):
        page = requests.get(page_config.get_serach_url(i))
        soup = BeautifulSoup(page.content, 'html.parser')

        ads = soup.find_all(page_config.bs4_block, attrs=page_config.bs4_attrs)
        ads_len = len(ads)
        if ads_len == 0:
            break

        with concurrent.futures.ThreadPoolExecutor(max_workers=ads_len) as executor:
            for ad in ads:
                executor.submit(listings.parse_listing_requests, ad, page_config)

def get_page_data(URL: str, page_config: PageRequest) -> Tuple[str, str]:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    info = soup.find_all(page_config.info_attributes_bs4_block, class_=page_config.info_attributes_bs4_class, attrs=page_config.info_attributes_bs4_attrs)[0]
    summary = soup.find_all(page_config.summary_attributes_bs4_block, class_=page_config.summary_attributes_bs4_class, attrs=page_config.summary_attributes_bs4_attrs)[0]
    
    if info != None:
        info = info.text.strip()
        summary = summary.text.strip()
        return (info, summary)
    
    return ('','')

def get_listing_entry(ad: element.Tag, reviewed_listings: dict, page_config: PageRequest) -> Tuple[Listing, bool]:
    href = ad.find_all(page_config.href_parser, href=True)[0]['href']
    URL = href if page_config.default_url == '' else page_config.default_url + href

    if URL in reviewed_listings:
        return None, False

    info, summary = get_page_data(URL, page_config)
    listing = Listing(page_url=URL,
                      summary=summary,
                      info=info)
    reviewed_listings[URL] = ''

    return listing, True
