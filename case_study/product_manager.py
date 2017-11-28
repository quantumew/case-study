"""
    Manages the business logic for products and calls through
    to the PersistanceManager.
"""

import os.path
import json
import jsonschema
from copy import deepcopy
from case_study.persistance_manager import PersistanceManager
from case_study.product_service_manager import ProductServiceManager
from case_study.errors import ProductNotFoundError, InvalidRequestError, ErrorResponse
from case_study.utils import load_json

class ProductManager(object):
    """
        Manages product related business logic.
    """
    def __init__(self, config, logger):
        """
            Args:
                self(case_study.persistance_manager.PersistanceManager)
                config(dict)
                logger(logging.logger)
        """
        self.config = config
        self.logger = logger
        db_config = self.config.get("database")
        self.persistance_manager = PersistanceManager(self.logger, db_config)
        endpoint = self.config.get('product_endpoint')
        qs = self.config.get('product_endpoint_exclude_fields')
        self.product_service_manager = ProductServiceManager(endpoint, qs)

    def get_product(self, product_id):
        """
            Queries for product from data store.

            Args:
                self(case_study.persistance_manager.PersistanceManager)
                product_id(int)

            Returns:
                dict: see ../schemas/product.json

            Raises:
                case_study.errors.ProductNotFoundError
        """
        product = self.persistance_manager.get_product_by_id(product_id)

        if not product:
            raise ProductNotFoundError('product with id "{}" was not found'.format(product_id))

        # Not necessary to send this to the client.
        product.pop('_id')
        name = self.product_service_manager.fetch_name(product_id)

        if name:
            product["name"] = name

        return product

    def persist_product(self, product_id, product):
        """
            Persists product to data store.

            Args:
                self(case_study.persistance_manager.PersistanceManager)
                product_id(int)
                product(dict): see ../schemas/product.json

            Raises:
                case_study.errors.InvalidRequestError
        """
        loaded_product = None

        try:
            loaded_product = self.validate_product(product)
        except jsonschema.ValidationError as err:
            raise InvalidRequestError(err.message)
        except:
            # Unlikely case but in case the schema cannot be found or the schema is flawed.
            raise ErrorResponse('internal server error')

        if loaded_product["id"] != product_id:
            raise InvalidRequestError('provided document id "{}" did not match id in request URL "{}"'.format(loaded_product["id"], product_id))

        self.persistance_manager.insert_product(deepcopy(loaded_product))
        name = self.product_service_manager.fetch_name(product_id)

        if name:
            loaded_product["name"] = name

        return loaded_product

    def validate_product(self, product):
        """
            Args:
                product(dict): see ../schemas/product.json

            Returns:
                dict
        """
        schema = load_json("schemas/product.json")
        loaded_product = json.loads(product)
        jsonschema.validate(loaded_product, schema)

        return loaded_product
