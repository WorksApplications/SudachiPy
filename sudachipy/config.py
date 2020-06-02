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


def unlink_default_dict_package(output, verbose=True):
    try:
        dst_path = Path(import_module('sudachidict').__file__).parent
    except ImportError:
        if verbose:
            print('Package `sudachidict` does not exist.', file=output)
        return

    if dst_path.is_symlink():
        dst_path.unlink()
        if verbose:
            print('Removed the package symbolic link `sudachidict`.', file=output)
    if dst_path.exists():
        raise IOError('Unlink failed (The `sudachidict` directory exists and it is not a symbolic link).')


def set_default_dict_package(dict_package, output):
    unlink_default_dict_package(output, verbose=False)

    src_path = Path(import_module(dict_package).__file__).parent
    dst_path = src_path.parent / 'sudachidict'
    dst_path.symlink_to(src_path)
    print('Set the default dictionary to `{}`.'.format(dict_package), file=output)

    return dst_path


def create_default_link_for_sudachidict_core(output):
    try:
        dict_path = Path(import_module('sudachidict').__file__).parent
    except ImportError:
        try:
            import_module('sudachidict_core')
        except ImportError:
            raise KeyError('You need to specify `systemDict` in the config when `sudachidict_core` is not installed.')
        try:
            import_module('sudachidict_full')
            raise KeyError('Multiple dictionaries installed. Set the default with `link -t` command.')
        except ImportError:
            pass
        try:
            import_module('sudachidict_small')
            raise KeyError('Multiple dictionaries installed. Set the default with `link -t` command.')
        except ImportError:
            pass
        dict_path = set_default_dict_package('sudachidict_core', output=output)
    return str(dict_path / 'resources' / 'system.dic')


class _Settings(object):

    def __init__(self):
        self.__is_active = False
        self.__dict_ = None
        self.resource_dir = None

    def set_up(self, path=None, resource_dir=None) -> None:
        path = path or DEFAULT_SETTINGFILE
        resource_dir = resource_dir or os.path.dirname(path)
        with open(path, 'r', encoding='utf-8') as f:
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
        key = 'systemDict'
        if key in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_[key])
        with open(os.devnull, 'w') as f:
            dict_path = create_default_link_for_sudachidict_core(output=f)
        self.__dict_[key] = dict_path
        return dict_path

    def char_def_path(self) -> str:
        key = 'characterDefinitionFile'
        if key in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_[key])
        raise KeyError('`{}` not defined in setting file'.format(key))

    def user_dict_paths(self) -> List[str]:
        key = 'userDict'
        if key in self.__dict_:
            return [os.path.join(self.resource_dir, path) for path in self.__dict_[key]]
        return []


settings = _Settings()
