from . import parse_json, parse_requests

from helpers.listings import Listings


class Parsers:
    def __init__(self, parser_type: str, page_config, listings: Listings) -> None:
        self.parser_type = parser_type
        self.page_config = page_config
        self.listings = listings

    def parse(self) -> None:
        if self.parser_type == 'requests':
            return parse_requests.parse(self.page_config, self.listings)
        if self.parser_type == 'json':
            return parse_json.parse(self.page_config, self.listings)
        if self.parser_type == 'selenium':
            return
        
        raise ValueError('parser_type unknown [{parser_type}]'.format(fname = self.page_config.parser_type))
