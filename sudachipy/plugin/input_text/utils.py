from typing import List

from sudachipy import config

from . import DefaultInputTextPlugin, InputTextPlugin, ProlongedSoundMarkInputTextPlugin


def get_input_text_plugin(json_obj) -> InputTextPlugin:
    # In the future, users can define plugin by themselves
    try:
        if json_obj['class'] == 'sudachipy.plugin.input_text.DefaultInputTextPlugin':
            return DefaultInputTextPlugin()
        if json_obj['class'] == 'sudachipy.plugin.input_text.ProlongedSoundMarkInputTextPlugin':
            return ProlongedSoundMarkInputTextPlugin(json_obj)
        raise ValueError('{} is invalid InputTextPlugin class'.format(json_obj['class']))
    except KeyError:
        raise ValueError('config file is invalid format')


def get_input_text_plugins() -> List[InputTextPlugin]:
    key_word = 'inputTextPlugin'
    if key_word not in config.settings:
        return []
    ps = []
    for obj in config.settings[key_word]:
        ps.append(get_input_text_plugin(obj))
    return ps
