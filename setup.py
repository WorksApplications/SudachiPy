from setuptools import setup, find_packages


setup(name="SudachiPy",
      version="0.1.2",
      description="Python version of Sudachi, the Japanese Morphological Analyzer",
      long_description="",
      url="https://github.com/WorksApplications/Sudachi",
      license="Apache-2.0",
      packages=find_packages(include=["sudachipy", "sudachipy.*"]),
      entry_points={
          "console_scripts": ["sudachipy=sudachipy.command_line:main"],
      },
      install_requires=["sortedcontainers>=2.1.0,<2.2.0"],
      include_package_data=True,
      )
