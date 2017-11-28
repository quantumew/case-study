Case Study
==========

This repository contains the solution for the myRetail case study. It utilizes Flask as a web framework and MongoDB as data store.


Running Application
-------------------

First you must have MongoDB installed and started see [here](https://docs.mongodb.com/manual/installation/). See [config file](./config.json) for default configuration details.

Running the following script will initialize the prototype database with prices and start the dev server.

    python bin/main.py


Running Tests
-------------

The following command will run the unit tests for the API.

    python tests/test.py


Endpoints
---------

GET on products.

    curl localhost:8080/products/16696650

    {
        "current_price": {
            "currency_code": "USD",
            "value": 23.00
        },
        "id": 16696650,
        "name": "Beats Solo 2 Wireless - White"
    }


PUT on products.

    curl localhost:8080/products/123456 -XPUT -d '{ "id": 123456, "current_price": { "currency_code": "USD", "value": 12.43 } }'

    {
        "current_price": {
            "currency_code": "USD",
            "value": 12.43
        },
        "id": 16696650,
        "name": "TEST"
    }

Notes
-----

The tests for this project are sufficient for prototype but in a production scenario more thorough unit testing would be required. Currently there are integration tests testing the API GET and PUT requests all of the way through. This was mostly because of time constraints.
