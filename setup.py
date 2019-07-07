from setuptools import setup, find_packages
from sudachipy import SUDACHIPY_VERSION

setup(name="SudachiPy",
      version=SUDACHIPY_VERSION,
      description="Python version of Sudachi, the Japanese Morphological Analyzer",
      long_description=open('README.md').read(),
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
            "sortedcontainers>=2.1.0,<2.2.0",
      ],
      )
