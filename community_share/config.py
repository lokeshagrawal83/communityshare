import json
import os


def load_app_config(key_list, filename):
    config = {}
    config.update(config_from_file(filename))
    config.update(config_from_env(key_list))

    return config


def config_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def config_from_env(key_list):
    return {
        key: value
        for key, value in os.environ.items()
        if key in key_list
    }
