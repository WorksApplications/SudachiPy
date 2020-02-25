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

from setuptools import setup, find_packages

setup(name="SudachiPy",
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description="Python version of Sudachi, the Japanese Morphological Analyzer",
      long_description=open('README.md', encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      url="https://github.com/WorksApplications/SudachiPy",
      license="Apache-2.0",
      author="Works Applications",
      author_email="takaoka_k@worksap.co.jp",
      packages=find_packages(include=["sudachipy", "sudachipy.*"]),
      package_data={"": ["resources/*.json", "resources/*.dic", "resources/*.def"]},
      entry_points={
          "console_scripts": ["sudachipy=sudachipy.command_line:main"],
      },
      install_requires=[
            "sortedcontainers~=2.1.0",
            'dartsclone~=0.9.0',
      ],
      )
