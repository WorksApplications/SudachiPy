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

from . import JoinKatakanaOovPlugin, JoinNumericPlugin, PathRewritePlugin


def get_path_rewrite_plugin(json_obj) -> PathRewritePlugin:
    # In the future, users can define plugin by themselves
    try:
        if json_obj['class'] == 'sudachipy.plugin.path_rewrite.JoinNumericPlugin':
            return JoinNumericPlugin(json_obj)
        if json_obj['class'] == 'sudachipy.plugin.path_rewrite.JoinKatakanaOovPlugin':
            return JoinKatakanaOovPlugin(json_obj)
        raise ValueError('{} is invalid PathRewritePlugin class'.format(json_obj['class']))
    except KeyError:
        raise ValueError('config file is invalid format')


def get_path_rewrite_plugins() -> List[PathRewritePlugin]:
    if 'pathRewritePlugin' not in config.settings:
        return []
    ps = []
    for obj in config.settings['pathRewritePlugin']:
        ps.append(get_path_rewrite_plugin(obj))
    return ps
