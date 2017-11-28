#!/usr/bin/env python
"""
    Starts case_study REST API for the prototyping period.
    It utilizes the persistance manager to initialize the document
    store with initial products.
"""

from case_study.app import app
from case_study.utils import load_docs

if __name__ == "__main__":
    load_docs()
    app.run(port=8080)
