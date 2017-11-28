"""
    Interface for interacting with document store.
"""

from pymongo import MongoClient

class PersistanceManager(object):
    def __init__(self, logger, db_config={}):
        """
            Args:
                self(case_study.persistance_manager.PersistanceManager)
                logger(logging.logger)
                db_config(dict)
        """
        self.logger = logger
        self.db_name = db_config.get("name", "case_study")
        self.host = db_config.get("host", "localhost")
        self.port = db_config.get("port", 27017)
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def insert_product(self, document):
        """
            Inserts a single document into document store.

            Args:
                self(case_study.persistance_manager.PersistanceManager)
                document(dict)

            Returns:
                dict
        """
        self.logger.info("Inserting provided document {}".format(document))
        result = self.db.products.insert_one(document)

        return result

    def get_product_by_id(self, product_id):
        """
            Retrieves product from document store using provided id.

            Args:
                self(case_study.persistance_manager.PersistanceManager)
                product_id(int)

            Returns:
                dict
        """
        self.logger.info("Querying for document with ID: {}".format(product_id))

        return self.db.products.find_one({"id": product_id})

    def insert_many_docs(self, payload):
        return self.db.products.insert_many(payload)
