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
