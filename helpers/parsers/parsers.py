from . import parse_json, parse_requests

from helpers.listings import Listings
from helpers.page import Page

class Parsers:
    def __init__(self, page_config: Page, listings: Listings) -> None:
        self.page_config = page_config
        self.listings = listings

    def parse(self) -> None:
        if self.page_config.parser_type == 'requests':
            return parse_requests.parse(self.page_config, self.listings)
        # if self.page_config.parser_type == 'selenium':
        #     return
        if self.page_config.parser_type == 'json':
            return parse_json.parse(self.page_config, self.listings)

        raise ValueError('parser_type unknown [{parser_type}]'.format(fname = self.page_config.parser_type))
