import json
import os


def get_config():

    file = "config.json"

    if not os.path.isfile(file):
        return None

    with open(file) as json_data:
        return json.load(json_data)
