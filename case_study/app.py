"""
    Entry point for myRetail prototype REST API. Sets up Flask app,
    registers blueprint for products, and configures app.
"""

from flask import Flask
from case_study.routes.products import products
from case_study import configure
from case_study.errors import ErrorResponse, InvalidRequestError, ProductNotFoundError

app = Flask(__name__)
app.register_blueprint(products)
configure.app(app)

@app.errorhandler(ErrorResponse)
@app.errorhandler(InvalidRequestError)
@app.errorhandler(ProductNotFoundError)
def generic_exception_handler(error):
    """
        Central spot for transmuting an internal error to an error response.
    """
    app.logger.exception(error)

    return error.to_vnd()
