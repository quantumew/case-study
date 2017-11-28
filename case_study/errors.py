"""
    Contains Errors that serve as representatives for HTTP errors.
"""

from flask import Response
import json

class ErrorResponse(Exception):
    """
        Error to be raised when a product is not found.
    """
    def __init__(self, message, error_code="INTERNAL_SERVER_ERROR", status_code=500):
        """
            Args:
                self(case_study.error.ErrorResponse)
        """
        super(ErrorResponse, self).__init__(message)
        self.error_code = error_code
        self.status_code = status_code
        self.message = message

    def to_vnd(self):
        """
            Converts internal error to vnd.error response.

            Args:
                self(case_study.error.ErrorResponse)
        """
        return vnd_error(self.error_code, self.message, self.status_code)

class ProductNotFoundError(ErrorResponse):
    """
        Error to be raised when a product is not found.
    """
    def __init__(self, message):
        """
            Args:
                self(case_study.error.ProductNotFoundError)
        """
        super(ProductNotFoundError, self).__init__(message, "PRODUCT_NOT_FOUND", 404)

class InvalidRequestError(ErrorResponse):
    """
        Error to be raised when an invalid request is made.
    """
    def __init__(self, message):
        """
            Args:
                self(case_study.error.InvalidRequestError)
        """
        super(InvalidRequestError, self).__init__(message, "BAD_REQUEST", 400)

def vnd_error(code, message, status_code):
    """
        Creates vnd.error type error response.
        https://github.com/blongden/vnd.error
    """
    body = json.dumps({
        "code": code,
        "message": message
    })
    response = Response()
    response.status_code = status_code
    response.set_data(body)

    return response
