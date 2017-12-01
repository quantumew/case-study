"""
    Tests for case_study.routes.products. Note these are integration tests with only the external
    calls to the product service mocked. Even the database is loaded with test data. This is mostly
    to provide solid integration tests that tests the entire API all of the way through. Perhaps
    after the prototyping period one may way to look into an in memory MongoDB mock service. Perhaps
    similar to moto onto boto for AWS services.
"""

import json
import unittest
import logging
import requests_mock
from urllib.parse import urljoin
from case_study.app import app
from case_study.utils import load_docs
from case_study.configure import app_config

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        # Lazily disabling logging for now for better deciphering of test output.
        config = {}
        app_config(config)
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()
        load_docs()
        self.valid_doc = {
            "id": 13860428,
            "name": "The Big Lebowski (Blu-ray)",
            "current_price": {
                "currency_code": "USD",
                "value": 13.49
            }
        }
        self.product_url = urljoin(config["product_endpoint"], str(self.valid_doc["id"])) + "?excludes={}".format(config["product_endpoint_exclude_fields"])
        self.valid_redsky_response = {
            "product": { "item": { "product_description": { "title": "The Big Lebowski (Blu-ray)"}}}
        }

    def test_get_entry(self):
        with requests_mock.mock() as m:
            m.get(self.product_url, text=json.dumps(self.valid_redsky_response))
            r = self.app.get("/products/{}".format(self.valid_doc["id"]))

        self.assertEqual(json.loads(r.get_data()), self.valid_doc)

    def test_get_entry_non_existant(self):
        r = self.app.get("/products/{}".format(1234))

        self.assertEqual(json.loads(r.get_data()), {"code": "PRODUCT_NOT_FOUND", "message": 'product with id "1234" was not found'})

    def test_put_entry(self):
        data = {
            "id": 13860428,
            "current_price": {
                "currency_code": "USD",
                "value": 100.00
            }
        }
        self.valid_doc["current_price"]["value"] = 100.00

        with requests_mock.mock() as m:
            m.get(self.product_url, text=json.dumps(self.valid_redsky_response))
            r = self.app.put("/products/{}".format(data["id"]), data=json.dumps(data))

        self.assertEqual(json.loads(r.get_data()), self.valid_doc)

    def test_put_entry_invalid_requests(self):
        data = {
            "id": 13860428,
            "current_price": {
                "the_money_thingy_ya_know_that_thing": "USD",
                "value": 100.00
            }
        }

        r = self.app.put("/products/{}".format(data["id"]), data=json.dumps(data))

        self.assertEqual(r.status_code, 400)

if __name__ == "__main__":
    unittest.main()
