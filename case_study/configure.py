"""
    Flask application configuration handler.
"""

import os
import logging
import json


def app_config(existing_config):
    """
        Reads and parses config file. Currently there is no schema validation but
        presumably that would be added after the prototyping period.

        existing_config(dict)
    """
    try:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config.json")
        config = json.load(open(config_path))
    except IOError:
        raise ValueError("Could not find or open file {0}".format(config_path))
    except:
        raise ValueError("{} contained invalid JSON".format(config_path))

    existing_config.update(config)


def app(flask_app):
    """
        Configures application using configuration file and sets up logger.

        Args:
            flask_app(flask.Flask)
    """
    app_config(flask_app.config)
    log_level_name = flask_app.config.get("log_level", "INFO")
    logger = logging.getLogger('case_study')
    logger.setLevel(log_level_name)
