from setuptools import setup, find_packages

setup(name="SudachiPy",
      version="0.2.1",
      description="Python version of Sudachi, the Japanese Morphological Analyzer",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url="https://github.com/WorksApplications/SudachiPy",
      license="Apache-2.0",
      author="Works Applications",
      author_email="takaoka_k@worksap.co.jp",
      packages=find_packages(include=["sudachipy", "sudachipy.*"]),
      entry_points={
          "console_scripts": ["sudachipy=sudachipy.command_line:main"],
      },
      install_requires=["sortedcontainers>=2.1.0,<2.2.0"],
      include_package_data=True,
      )
