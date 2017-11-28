"""
    Routes for '/products'.
"""

import json
from flask import request, Blueprint, Response
from flask import current_app
from case_study.product_manager import ProductManager

products = Blueprint("products", __name__)

@products.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
        Endpoint for retreiving products by ID.
        All error scenarios are handled in a generic handler.
    """
    product_manager = ProductManager(current_app.config, current_app.logger)
    response = Response(content_type="application/json")
    data = product_manager.get_product(product_id)
    data = json.dumps(data)
    response.set_data(data)
    response.status_code = 200

    return response

@products.route("/products/<int:product_id>", methods=["PUT"])
def put_product(product_id):
    """
        Endpoint for creating/updating products by ID.
        All error scenarios are handled in a generic handler.
    """
    product_manager = ProductManager(current_app.config, current_app.logger)
    response = Response(content_type="application/json")
    new_product = product_manager.persist_product(product_id, request.get_data())
    response.status_code = 201
    response.set_data(json.dumps(new_product))

    return response
