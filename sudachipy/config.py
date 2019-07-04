import json
import os
from typing import List

DEFAULT_SETTINGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "resources/sudachi.json")
DEFAULT_RESOURCEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "resources")


class _Settings(object):

    def __init__(self):
        self.__is_active = False
        self.__dict_ = None
        self.resource_dir = DEFAULT_RESOURCEDIR

    def set_up(self, path=None, resource_dir=None) -> None:
        if not path:
            path = DEFAULT_SETTINGFILE
        if not resource_dir:
            resource_dir = DEFAULT_RESOURCEDIR
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

    def system_dict_path(self) -> str:
        if 'systemDict' in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_['systemDict'])
        raise KeyError('`systemDict` not defined in setting file')

    def char_def_path(self) -> str:
        if 'characterDefinitionFile' in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_['characterDefinitionFile'])
        raise KeyError('`characterDefinitionFile` not defined in setting file')

    def user_dict_paths(self) -> List[str]:
        if 'userDict' in self.__dict_:
            return [os.path.join(self.resource_dir, path) for path in self.__dict_['userDict']]
        return []


settings = _Settings()
