# Copyright (c) 2019 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from importlib import import_module
from pathlib import Path
from typing import List

DEFAULT_RESOURCEDIR = Path(__file__).absolute().parent / 'resources'
DEFAULT_SETTINGFILE = DEFAULT_RESOURCEDIR / 'sudachi.json'
DEFAULT_RESOURCEDIR = DEFAULT_RESOURCEDIR.as_posix()
DEFAULT_SETTINGFILE = DEFAULT_SETTINGFILE.as_posix()


def set_dict_package(dict_type: str, output) -> None:
    """Rewrite config file to change dictionary
    Args:
        dict_type (str): full, core, small
        output: like sys.stdout
    Returns:
        None
    Throws:
        ImportError if dictionary not installed as python package
    """
    pkg_path = Path(import_module('sudachidict_' + dict_type).__file__).parent
    dic_path = pkg_path / 'resources' / 'system.dic'
    settings[settings.DICT_PATH_KEY] = dic_path.absolute().as_posix()
    settings.rewrite_config()
    return


class _Settings(object):
    """ Map like interface to manage configuration arguments between json and python
    """

    DICT_PATH_KEY = 'systemDict'
    CHAR_DEF_KEY = 'characterDefinitionFile'
    USER_DICT_PATH_KEY = 'userDict'

    __path = None
    __is_active = False
    __dict_ = None
    resource_dir = None

    def __init__(self):
        return

    def set_up(self, path=None, resource_dir=None) -> None:
        """
        Args:
            path(str): path to config file, PACKAGE/sudachipy/resources/sudachi.json used in default
        """
        path = path or DEFAULT_SETTINGFILE
        self.__path = path
        resource_dir = resource_dir or os.path.dirname(path)
        with open(path, 'r', encoding='utf-8') as f:
            self.__dict_ = json.load(f)
        self.__is_active = True
        self.resource_dir = resource_dir

    def __setitem__(self, key, value):
        if not self.__is_active:
            self.set_up()
        self.__dict_[key] = value

    def __getitem__(self, key):
        if not self.__is_active:
            self.set_up()
        return self.__dict_[key]

    def keys(self):
        return self.__dict_.keys()

    def __contains__(self, item):
        return item in self.__dict_.keys()

    def rewrite_config(self):
        """ Rewrites config file with current setting
        """
        with open(self.__path, 'w') as f:
            json.dump(self.__dict_, f)

    def system_dict_path(self) -> str:
        key = self.DICT_PATH_KEY
        if key in self.__dict_:
            value = self.__dict_[key]
            if value.startswith('/'):
                return value
            return os.path.join(self.resource_dir, value)
        raise KeyError('{} not defined in setting file'.format(key))

    def char_def_path(self) -> str:
        key = self.CHAR_DEF_KEY
        if key in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_[key])
        raise KeyError('`{}` not defined in setting file'.format(key))

    def user_dict_paths(self) -> List[str]:
        key = self.USER_DICT_PATH_KEY
        if key in self.__dict_:
            return [os.path.join(self.resource_dir, path) for path in self.__dict_[key]]
        return []


settings = _Settings()
