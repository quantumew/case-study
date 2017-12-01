"""
    This service manages the interaction with the internal product service.
"""

from urllib.parse import urljoin
import requests
from case_study.errors import ProductNotFoundError

class ProductServiceManager(object):
    def __init__(self, endpoint, qs):
        """
            Args:
               self(case_study.product_service_manager.ProductServiceManager)
               endpoint(string)
               qs(string)
        """
        # Validate endpoint
        self.endpoint = endpoint
        self.query_string = qs

    def fetch_name(self, product_id):
        """
            Args:
                self(case_study.product_service_manager.ProductServiceManager)
                product_id(int)
        """
        product_url = urljoin(self.endpoint, str(product_id)) + "?excludes={}".format(self.query_string)
        result = requests.get(product_url)

        if result.status_code != requests.codes["ok"]:
            raise ProductNotFoundError("could not find product name for ID {}".format(product_id))

        data = result.json()

        try:
            name = data["product"]["item"]["product_description"]["title"]
        except KeyError:
           name = None

        return name
