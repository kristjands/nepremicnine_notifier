import json
from typing import Dict, List

import helpers.config_defaults as defaults


class Page:
    def __init__(self, page):
        self.parser_type = page['parser_type'] if 'parser_type' in page else defaults.parser_type
        self.key = page['key']
        
        self.to_email = page['to_email']
        self.from_email = page['from_email']
        self.gmail_api_key = page['gmail_api_key']
        self.default_url = page['default_url']
        self.page_url = page['page_url']
        self.admin_mail = page['admin_mail'] if 'admin_mail' in page else page['from_email']
        self.mail_subject = page['mail_subject'] if 'mail_subject' in page else defaults.mail_subject

        self.bs4_block = page['bs4_block'] if 'bs4_block' in page else defaults.bs4_block
        self.href_parser = page['href_parser'] if 'href_parser' in page else defaults.href_parser
        self.bs4_attrs = page['bs4_attrs'] if 'bs4_attrs' in page else defaults.bs4_attrs
        self.info_attributes_bs4_block = page['info_attributes']['bs4_block'] if 'info_attributes' in page and 'bs4_block' in page['info_attributes'] else defaults.info_attributes_bs4_block
        self.info_attributes_bs4_attrs = page['info_attributes']['bs4_attrs'] if 'info_attributes' in page and 'bs4_attrs' in page['info_attributes'] else defaults.info_attributes_bs4_attrs
        self.info_attributes_bs4_class = page['info_attributes']['bs4_class'] if 'info_attributes' in page and 'bs4_class' in page['info_attributes'] else defaults.info_attributes_bs4_class

        self.summary_attributes_bs4_block = page['summary_attributes']['bs4_block'] if 'summary_attributes' in page and 'bs4_block' in page['summary_attributes'] else defaults.summary_attributes_bs4_block
        self.summary_attributes_bs4_attrs = page['summary_attributes']['bs4_attrs'] if 'summary_attributes' in page and 'bs4_attrs' in page['summary_attributes'] else defaults.summary_attributes_bs4_attrs
        self.summary_attributes_bs4_class = page['summary_attributes']['bs4_class'] if 'summary_attributes' in page and 'bs4_class' in page['summary_attributes'] else defaults.summary_attributes_bs4_class

        self.json_request_method = page['json']['method'] if 'json' in page and 'method' in page['json'] else None
        self.json_post_body = page['json']['post_body'] if 'json' in page and 'post_body' in page['json'] else None
        self.json_pagination_name = page['json']['pagination_name'] if 'json' in page and 'pagination_name' in page['json'] else None
        self.json_pagination_offset = page['json']['pagination_offset'] if 'json' in page and 'pagination_offset' in page['json'] else None
        self.json_pagination_offset_name = page['json']['pagination_offset_name'] if 'json' in page and 'pagination_offset_name' in page['json'] else None
        self.json_pagination_limit = page['json']['pagination_limit'] if 'json' in page and 'pagination_limit' in page['json'] else None
        self.json_pagination_limit_name = page['json']['pagination_limit_name'] if 'json' in page and 'pagination_limit_name' in page['json'] else None
        self.json_pagination_count_all_name = page['json']['pagination_count_all_name'] if 'json' in page and 'pagination_count_all_name' in page['json'] else None
        self.json_result_name = page['json']['result_name'] if 'json' in page and 'result_name' in page['json'] else None
        self.json_info_attributes = page['json']['info_attributes'] if 'json' in page and 'info_attributes' in page['json'] else None
        
    def get_serach_url(self, i :int) -> str:
        return f'{self.page_url}/{i}/'


def check_fields(page: Dict) -> None:
    keys = ['key', 'to_email', 'from_email', 'default_url', 'page_url', 'gmail_api_key']
    for key in keys:
        if key not in page:
            raise Exception(f'Missing {key} parameter in configuration')

def load_configs() -> None:
    with open('./configuration.json') as json_file:
        for page in json.load(json_file)['pages']:
            yield Page(page)
