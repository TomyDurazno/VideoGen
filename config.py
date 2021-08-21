import json
import os


def get_config():
    if not os.path.isfile('config.json'):
        return None

    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
        return data
