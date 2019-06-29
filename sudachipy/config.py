import json
import os

SETTINGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "resources/sudachi.json")
RESOURCEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "resources")


class _Settings(object):

    def __init__(self):
        self.__is_active = False
        self.__dict_ = None
        self.resource_dir = RESOURCEDIR

    def set_up(self, path=SETTINGFILE, resource_dir=RESOURCEDIR):
        with open(path, "r", encoding="utf-8") as f:
            self.__dict_ = json.load(f)
        self.__is_active = True
        self.resource_dir = resource_dir

    def __getitem__(self, key):
        if not self.__is_active:
            self.set_up()
        return self.__dict_[key]

    def keys(self):
        return self.__dict_.keys()

    def __contains__(self, item):
        return item in self.__dict_.keys()

    def has(self, key):
        return key in self.__dict_


settings = _Settings()
