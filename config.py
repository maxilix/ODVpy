import json

from settings import *


class CONFIG(object):
    installation_path: str = ""
    backup_path: str = "backup"
    automatically_load_original_dvm: bool = True
    default_tabs: list = []

    @classmethod
    def load(cls):
        try:
            with open(CONFIG_FILENAME, "r") as json_file:
                data = json.load(json_file)
            cls.installation_path = data["installation_path"]
            cls.backup_path = data["backup_path"]
            cls.automatically_load_original_dvm = bool(data["automatically_load_original_dvm"])
            cls.default_tabs = list(set(data["default_tabs"]) - {"DVM"})
        except (FileNotFoundError, json.JSONDecodeError):
            print("Default Config")

    @classmethod
    def save(cls):
        data = dict()
        data["installation_path"] = cls.installation_path
        data["backup_path"] = cls.backup_path
        data["automatically_load_original_dvm"] = cls.automatically_load_original_dvm
        data["default_tabs"] = cls.default_tabs
        with open(CONFIG_FILENAME, "w") as json_file:
            json.dump(data, json_file, indent=2)
