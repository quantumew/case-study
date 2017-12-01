Case Study
==========

This repository contains the solution for the myRetail case study. It utilizes Flask as a web framework and MongoDB as data store.


Running Application
-------------------

First you must have MongoDB installed and started see [here](https://docs.mongodb.com/manual/installation/). See [config file](./config.json) for default configuration details.

During the development period it is recommended that virtualenv is used. Run the following script to install the appropriate dependencies and activate your virtual environment.

    source utils/init-environment

Running the following script will initialize the prototype database with prices and start the dev server.

    python bin/main.py


Running Tests
-------------

The following command will run the unit tests for the API.

    python tests/test.py


Product Name
------------

The product name is retrieved from an internal service on PUT and GET. This is to provide the proper response to the user but it is not persisted in the application data store.

Endpoints
---------

GET on products.

    curl localhost:8080/products/16696650 | jq

    {
        "current_price": {
            "currency_code": "USD",
            "value": 23.00
        },
        "id": 16696650,
        "name": "Beats Solo 2 Wireless - White"
    }


PUT on products. Note: PUT is considered an update so existing records will be updated but after killing the instance of the server and restarting the data will be reverted to the original test data. This is simply to provide a good experience during the prototyping phase.

    curl localhost:8080/products/123456 -XPUT -d '{ "id": 123456, "current_price": { "currency_code": "USD", "value": 12.43 } }' | jq

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
