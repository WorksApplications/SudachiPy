from setuptools import setup

def readme():
      with open("README.md", encoding="utf-8") as f:
            return f.read()

setup(name="SudachiPy",
      version="0.1.0",
      description="Python version of Sudachi, the Japanese Morphological Analyzer",
      long_description=readme(),
      url="https://github.com/WorksApplications/Sudachi",
      license="Apache-2.0",
      packages=["sudachipy"],
      entry_points = {
            "console_scripts": ["sudachipy=sudachipy.command_line:main"],
      },
      include_package_data=True,
      )