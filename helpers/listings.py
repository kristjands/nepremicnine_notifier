import threading

from helpers.parsers.parse_requests import get_listing_entry as page_parser_requests
from helpers.parsers.parse_json import get_listing_entry as page_parser_json
from helpers.page import PageRequest, PageJson


class Listings:
    def __init__(self, reviewed_listings: dict):
        self._reviewed_listings = reviewed_listings
        self._listings_to_report = list()
        self._lock = threading.Lock()
    
    def parse_listing_requests(self, ad, page_config: PageRequest):
        listing, success = page_parser_requests(ad, self._reviewed_listings, page_config)
        with self._lock:
            if success:
                self._listings_to_report.append(listing)
    
    def parse_listing_json(self, ad, page_config: PageJson):
        listing, success = page_parser_json(ad, self._reviewed_listings, page_config)
        with self._lock:
            if success:
                self._listings_to_report.append(listing)

    def generate_email(self) -> str:
        return '\n'.join([listing.report() for listing in self._listings_to_report])

    def get_reviewed_listings(self) -> dict:
        return self._reviewed_listings
