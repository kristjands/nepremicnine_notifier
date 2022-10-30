import requests
from bs4 import BeautifulSoup, element
from typing import Tuple

from helpers.page import Page
from helpers.listing import Listing


def get_page_data(URL: str, page_config: Page, ad: element.Tag) -> Tuple[str, str]:
    info, summary = None, None

    if not page_config.summary_in_ad:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        info_list = soup.find_all(page_config.info_attributes_bs4_block, class_=page_config.info_attributes_bs4_class, attrs=page_config.info_attributes_bs4_attrs)
        summary_list = soup.find_all(page_config.summary_attributes_bs4_block, class_=page_config.summary_attributes_bs4_class, attrs=page_config.summary_attributes_bs4_attrs)
    else:
        info_list = ad.find_all(page_config.info_attributes_bs4_block, class_=page_config.info_attributes_bs4_class, attrs=page_config.info_attributes_bs4_attrs)
        summary_list = ad.find_all(page_config.summary_attributes_bs4_block, class_=page_config.summary_attributes_bs4_class, attrs=page_config.summary_attributes_bs4_attrs)
    
    if len(info_list) == 0 and len(summary_list) == 0:
        return ('', '')

    if len(info_list) > 0:
        info = info_list[0]
    if len(summary_list) > 0:
        summary = summary_list[0]

    info = info.text.strip() if info != None else ''
    summary = summary.text.strip() if summary != None else ''
    
    return (info, summary)
    
def get_listing_entry(ad: element.Tag, reviewed_listings: dict, page_config: Page) -> Tuple[Listing, bool]:
    href_list = ad.find_all(page_config.href_parser, href=True)
    if len(href_list) > 0: # href is in child elements
        href = href[0]['href']
    elif 'href' in ad.attrs: # href is in current element
        href = ad.attrs['href']
    else:
        return None, False # Received invalid element with no URL

    URL = href if page_config.default_url == "" else page_config.default_url + href

    if URL in reviewed_listings:
        return None, False

    info, summary = get_page_data(URL, page_config, ad)
    listing = Listing(page_url=URL,
                    summary=summary,
                    info=info)
    reviewed_listings[URL] = ''

    return listing, True
