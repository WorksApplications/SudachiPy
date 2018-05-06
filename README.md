# SudachiPy

SudachiPy is a Python version of [Sudachi](https://github.com/WorksApplications/Sudachi), a Japanese morphological analyzer.

Sudachi & SudachiPy are developed in [WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/), an institute under [Works Applications](http://www.worksap.com/) that focuses on Natural Language Processing (NLP).

Warning: SudachiPy is still under development, and some of the functions are still not complete. Please use it at your own risk.


## Instruction

SudachiPy requires Python3.5+.

SudachiPy is not registered to PyPI just yet, so you may not install it via `pip` command at the moment.

Here is instruction of installing.

1. `git clone https://github.com/WorksApplications/SudachiPy.git`
2. `make` to put system dictionary
3. `python setup.py install`

The dictionary file is not included in the repository. You can get the built dictionary from [Releases · WorksApplications/Sudachi](https://github.com/WorksApplications/Sudachi/releases). Please download either `sudachi-x.y.z-dictionary-core.zip` or `sudachi-x.y.z-dictionary-full.zip`, unzip and rename it to `system.dic`, then place it under `SudachiPy/resources/`.

After installing SudachiPy, you may also use it in the terminal via command `sudachipy`.

```
$ sudachipy -h
usage: sudachipy [-h] [-r file] [-m {A,B,C}] [-o file] [-a] [-d] [-v] ...

Japanese Morphological Analyzer

positional arguments:
  input file(s)

optional arguments:
  -h, --help     show this help message and exit
  -r file        the setting file in JSON format
  -m {A,B,C}     the mode of splitting
  -o file        the output file
  -a             print all of the fields
  -d             print the debug information
  -v, --version  show program's version number and exit

```
