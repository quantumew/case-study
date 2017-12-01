import json
import os
import logging
from case_study.persistance_manager import PersistanceManager
from case_study.configure import app_config

def load_json(path):
    """
        Loads JSON file with path relative to base directory.

        Args:
            path(string)

        Returns:
            object
    """
    directory_of_this_file = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(directory_of_this_file, "../", path)
    full_path = os.path.realpath(full_path)

    with open(full_path, "r") as f:
        data = f.read()

    return json.loads(data)

def load_docs():
    """
        Loads test documents for prototype. See ../data/test-data.json
    """
    config = {}
    app_config(config)
    logging.basicConfig(level=config.get("log_level"))
    persistance_manager = PersistanceManager(logging, config.get("database"))
    data = load_json("./data/test-data.json")
    persistance_manager.upsert_many_docs(data)
