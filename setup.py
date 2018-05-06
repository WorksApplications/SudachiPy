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
      # or you can use find_all() function here to extract all py module files.
      packages=["sudachipy", "sudachipy.dictionarylib", "sudachipy.dartsclone",
                "sudachipy.plugin", "sudachipy.plugin.input_text", "sudachipy.plugin.oov", "sudachipy.plugin.path_rewrite",
                "resources"],
      package_data={"resources": ["*"]},
      entry_points = {
            "console_scripts": ["sudachipy=sudachipy.command_line:main"],
      },
      include_package_data=True,
      )