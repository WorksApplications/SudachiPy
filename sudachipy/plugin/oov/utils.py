from . import OovProviderPlugin, MeCabOovPlugin, SimpleOovPlugin


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
