import concurrent.futures
import json
import requests
from typing import Tuple

from helpers.page import PageJson
from helpers.listing import Listing


def parse(page_config: PageJson, listings) -> None:
    fetched_listings = []
    max_requests = page_config.number_of_cycles if page_config.number_of_cycles is not None else 100000
    for i in range(0, max_requests):
        json_body = json.loads(page_config.post_body)

        if page_config.pagination_offset_name is not None and page_config.pagination_limit_name is not None \
            and page_config.pagination_offset is not None and page_config.pagination_limit is not None:
            if page_config.pagination_name is None:
                json_body[page_config.pagination_offset_name] = int(page_config.pagination_offset) + int(page_config.pagination_limit) * i
                json_body[page_config.pagination_limit_name] = int(page_config.pagination_limit)
            else:
                json_add = json.loads('{}')
                json_add[page_config.pagination_offset_name] = int(page_config.pagination_offset) + int(page_config.pagination_limit) * i
                json_add[page_config.pagination_limit_name] = int(page_config.pagination_limit)

                json_body[page_config.pagination_name] = json_add
        
        response = requests.post(page_config.page_url, json=json_body)

        response_json = json.loads(response.text)
        fetched_listings.extend(response_json[page_config.result_name])

        if page_config.pagination_response_name is not None and page_config.pagination_response_name in response_json:
            if page_config.pagination_count_all_name is not None:
                if page_config.pagination_count_all_name in response_json[page_config.pagination_response_name]:
                    all_items = int(response_json[page_config.pagination_response_name][page_config.pagination_count_all_name])
            else:
                all_items = int(response_json[page_config.pagination_response_name])
            
            if (i + 1) * int(page_config.pagination_limit) >= all_items:
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

    if page_config.info_attributes is not None:
        for info_item in page_config.info_attributes.split(','):
            if info_item in flatten_json:
                info += '{0}: {1}\n'.format(info_item, flatten_json[info_item])
    else:
        for key in flatten_json:
            info += '{0}: {1}\n'.format(key, flatten_json[key])
    
    if info != None:
        info = info.strip()
        summary = summary.strip()
        return (info, summary)
    
    return ('','')

def get_listing_entry(ad, reviewed_listings: dict, page_config: PageJson) -> Tuple[Listing, bool]:
    postfix = page_config.url_postfix if page_config.url_postfix is not None and page_config.url_postfix != '' else ''
    for macro in page_config.url_postfix_macros.split(','):
        if macro in ad:
            postfix = postfix.replace('{:%s}' % macro, ad[macro])

    URL = '{0}{1}'.format(page_config.default_url, postfix)

    if URL in reviewed_listings:
        return None, False

    info, summary = get_page_data(ad, page_config)
    listing = Listing(page_url=URL,
                      summary=summary,
                      info=info)
    reviewed_listings[URL] = ''

    return listing, True
