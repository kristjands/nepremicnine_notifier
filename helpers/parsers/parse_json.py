import json
import requests

from ..page import Page
from ..listings import Listings

def parse(page_config: Page, listings: Listings) -> None:
    for i in range(0, 1000):
        json_body = json.loads(page_config.json_post_body)

        json_add = json.loads('{}')
        json_add[page_config.json_pagination_offset_name] = int(page_config.json_pagination_offset) + int(page_config.json_pagination_limit) * i
        json_add[page_config.json_pagination_limit_name] = int(page_config.json_pagination_limit)

        json_body[page_config.json_pagination_name] = json_add
        
        response = requests.post(page_config.page_url, json=json_body, headers={'Content-Type': 'application/json', 'Accept': '*/*'})
        print(response)