from typing import List

from sudachipy import config

from . import MeCabOovPlugin, OovProviderPlugin, SimpleOovPlugin


def get_oov_plugin(json_obj) -> OovProviderPlugin:
    # In the future, users can define plugin by themselves
    try:
        if json_obj['class'] == 'sudachipy.plugin.oov.MeCabOovProviderPlugin':
            return MeCabOovPlugin(json_obj)
        if json_obj['class'] == 'sudachipy.plugin.oov.SimpleOovProviderPlugin':
            return SimpleOovPlugin(json_obj)
        raise ValueError('{} is invalid OovProviderPlugin class'.format(json_obj['class']))
    except KeyError:
        raise ValueError('config file is invalid format')


def get_oov_plugins() -> List[OovProviderPlugin]:
    key_word = 'oovProviderPlugin'
    if key_word not in config.settings:
        return []
    ps = []
    for obj in config.settings[key_word]:
        ps.append(get_oov_plugin(obj))
    return ps
