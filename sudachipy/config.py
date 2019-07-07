import json
import os
from importlib import import_module
from pathlib import Path
from typing import List

DEFAULT_SETTINGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/sudachi.json")
DEFAULT_RESOURCEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")


def unlink_default_dict_package(output):
    try:
        dst_path = Path(import_module('sudachidict').__file__).parent
    except ImportError:
        print('sudachidict not exists', file=output)
        return

    if dst_path.is_symlink():
        print('unlinking sudachidict', file=output)
        dst_path.unlink()
        print('sudachidict unlinked', file=output)
    if dst_path.exists():
        raise IOError('unlink failed (directory exists)')


def set_default_dict_package(dict_package, output):
    unlink_default_dict_package(output)

    src_path = Path(import_module(dict_package).__file__).parent
    dst_path = src_path.parent / 'sudachidict'
    dst_path.symlink_to(src_path)
    print('default dict package = {}'.format(dict_package), file=output)

    return dst_path


def create_default_link_for_sudachidict_core(output):
    try:
        dict_path = Path(import_module('sudachidict').__file__).parent
    except ImportError:
        try:
            import_module('sudachidict_core')
        except ImportError:
            raise KeyError('`systemDict` must be specified if `SudachiDict_core` not installed')
        try:
            import_module('sudachidict_full')
            raise KeyError('Multiple packages of `SudachiDict_*` installed. Set default dict with link command.')
        except ImportError:
            pass
        try:
            import_module('sudachidict_small')
            raise KeyError('Multiple packages of `SudachiDict_*` installed. Set default dict with link command.')
        except ImportError:
            pass
        dict_path = set_default_dict_package('sudachidict_core', output=output)
    return str(dict_path / 'resources' / 'system.dic')


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
        else:
            with open(os.devnull, 'w') as f:
                dict_path = create_default_link_for_sudachidict_core(output=f)
            self.__dict_['systemDict'] = dict_path
            return dict_path

    def char_def_path(self) -> str:
        if 'characterDefinitionFile' in self.__dict_:
            return os.path.join(self.resource_dir, self.__dict_['characterDefinitionFile'])
        raise KeyError('`characterDefinitionFile` not defined in setting file')

    def user_dict_paths(self) -> List[str]:
        if 'userDict' in self.__dict_:
            return [os.path.join(self.resource_dir, path) for path in self.__dict_['userDict']]
        return []


settings = _Settings()
