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
import warnings
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import List

DEFAULT_RESOURCEDIR = Path(__file__).absolute().parent / 'resources'
DEFAULT_SETTINGFILE = DEFAULT_RESOURCEDIR / 'sudachi.json'
DEFAULT_RESOURCEDIR = DEFAULT_RESOURCEDIR.as_posix()
DEFAULT_SETTINGFILE = DEFAULT_SETTINGFILE.as_posix()


def get_absolute_dict_path(dict_type: str) -> str:
    pkg_path = Path(import_module('sudachidict_' + dict_type).__file__).parent
    dic_path = pkg_path / 'resources' / 'system.dic'
    return str(dic_path.absolute())


def to_absolute_resource_path(resource_dir: str, dict_path: str) -> str:
    if Path(dict_path).is_absolute():
        return dict_path
    else:
        return os.path.join(resource_dir, dict_path)


def find_dict_path(dict_type='core'):
    is_installed = find_spec('sudachidict_{}'.format(dict_type))
    if is_installed:
        return get_absolute_dict_path(dict_type)
    else:
        raise ModuleNotFoundError(
            'Package `sudachidict_{}` dose not exist. '
            'You may install it with a command `$ pip install sudachidict_{}`'.format(dict_type, dict_type)
        )


class _Settings(object):

    DICT_PATH_KEY = 'systemDict'
    CHAR_DEF_KEY = 'characterDefinitionFile'
    USER_DICT_PATH_KEY = 'userDict'

    def __init__(self):
        self.__is_active = False
        self.__dict_ = None
        self.__config_path = None
        self.resource_dir = None

    def set_up(self, config_path=None, resource_dir=None, dict_type=None) -> None:
        config_path = config_path or DEFAULT_SETTINGFILE
        self.__config_path = config_path
        resource_dir = resource_dir or os.path.dirname(config_path)
        with open(config_path, 'r', encoding='utf-8') as f:
            self.__dict_ = json.load(f)
        self.__is_active = True
        self.resource_dir = resource_dir
        if dict_type is not None:
            if dict_type in ['small', 'core', 'full']:
                if self.DICT_PATH_KEY in self.__dict_ and self.__dict_[self.DICT_PATH_KEY] and \
                        'sudachidict_{}'.format(dict_type) not in self.__dict_[self.DICT_PATH_KEY]:
                    warnings.warn(
                        'Two system dictionaries may be specified. '
                        'The `sudachidict_{}` defined "dict_type" overrides those defined in the config file.'.format(dict_type)
                    )
                self.__dict_[self.DICT_PATH_KEY] = find_dict_path(dict_type=dict_type)
            else:
                raise ValueError('"dict_type" must be "small", "core", or "full".')
        else:
            if self.DICT_PATH_KEY not in self.__dict_ or not self.__dict_[self.DICT_PATH_KEY]:
                self.__dict_[self.DICT_PATH_KEY] = find_dict_path()

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

    def system_dict_path(self) -> str:
        dict_path = self.__dict_[self.DICT_PATH_KEY]
        return to_absolute_resource_path(self.resource_dir, dict_path)

    def char_def_path(self) -> str:
        key = self.CHAR_DEF_KEY
        if key in self.__dict_:
            return to_absolute_resource_path(self.resource_dir, self.__dict_[key])
        raise KeyError('`{}` not defined in setting file'.format(key))

    def user_dict_paths(self) -> List[str]:
        key = self.USER_DICT_PATH_KEY
        if key in self.__dict_:
            return [to_absolute_resource_path(self.resource_dir, path) for path in self.__dict_[key]]
        return []


settings = _Settings()
