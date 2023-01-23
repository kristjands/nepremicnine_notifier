import concurrent.futures
import json
import requests
from typing import Tuple

from helpers.page import PageJson
from helpers.listing import Listing

def parse(page_config: PageJson, listings) -> None:
    fetched_listings = []
    for i in range(0, 1000):
        json_body = json.loads(page_config.json_post_body)

        json_add = json.loads('{}')
        json_add[page_config.json_pagination_offset_name] = int(page_config.json_pagination_offset) + int(page_config.json_pagination_limit) * i
        json_add[page_config.json_pagination_limit_name] = int(page_config.json_pagination_limit)

        json_body[page_config.json_pagination_name] = json_add
        
        response = requests.post(page_config.page_url, json=json_body)

        response_json = json.loads(response.text)
        fetched_listings.extend(response_json[page_config.json_result_name])

        if page_config.json_pagination_name in response_json:
            if page_config.json_pagination_count_all_name in response_json[page_config.json_pagination_name]:
                all_items = int(response_json[page_config.json_pagination_name][page_config.json_pagination_count_all_name])
                if (i + 1) * int(page_config.json_pagination_limit) >= all_items:
                    break
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(fetched_listings)) as executor:
        for listing in fetched_listings:
            executor.submit(listings.parse_listing_json, listing, page_config)

def flatten_data(data):
    out = {}

    def flatten(node, name=''):
        if type(node) is dict:
            for item in node:
                flatten(node[item], name + item + '_')
        elif type(node) is list:
            i = 0
            for item in node:
                flatten(item, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = node

    flatten(data)
    return out

def get_page_data(ad, page_config: PageJson) -> Tuple[str, str]:
    flatten_json = flatten_data(ad)
    info = ''
    summary = ''

    for info_item in page_config.json_info_attributes.split(','):
        if info_item in flatten_json:
            info += '{0}: {1}\n'.format(info_item, flatten_json[info_item])
    
    if info != None:
        info = info.strip()
        summary = summary.strip()
        return (info, summary)
    
    return ('','')

def get_listing_entry(ad, reviewed_listings: dict, page_config: PageJson) -> Tuple[Listing, bool]:
    postfix = ''
    for attribute in page_config.json_url_attributes.split(','):
        postfix += ad[attribute] + '/'
        
    URL = '{0}{1}'.format(page_config.default_url, postfix)

    if URL in reviewed_listings:
        return None, False

    info, summary = get_page_data(ad, page_config)
    listing = Listing(page_url=URL,
                      summary=summary,
                      info=info)
    reviewed_listings[URL] = ''

    return listing, True
