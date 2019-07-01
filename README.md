# SudachiPy
[![Build Status](https://travis-ci.com/WorksApplications/SudachiPy.svg?branch=develop)](https://travis-ci.com/WorksApplications/SudachiPy)

SudachiPy is a Python version of [Sudachi](https://github.com/WorksApplications/Sudachi), a Japanese morphological analyzer.

Sudachi & SudachiPy are developed in [WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/), an institute under [Works Applications](http://www.worksap.com/) that focuses on Natural Language Processing (NLP).

**Warning: SudachiPy is still under development, and some of the functions are still not complete. Please use it at your own risk.**


## Setup

SudachiPy requires Python3.5+.

SudachiPy is not registered to PyPI just yet, so you may not install it via `pip` command at the moment.

```
$ pip install -e git+git://github.com/WorksApplications/SudachiPy@develop#egg=SudachiPy
```
The dictionary file is not included in the repository. You can get the built dictionary from [Releases · WorksApplications/Sudachi](https://github.com/WorksApplications/Sudachi/releases). Please download either `sudachi-x.y.z-dictionary-core.zip` or `sudachi-x.y.z-dictionary-full.zip`, unzip and rename it to `system.dic`, then place it under `SudachiPy/resources/`. In the end, we would like to make a flow to get these resources via the code, like [NLTK](https://www.nltk.org/data.html) (e.g., `import nltk; nltk.download()`) or [spaCy](https://spacy.io/usage/models) (e.g., `$python -m spacy download en`).

## Usage

### As a command

After installing SudachiPy, you may also use it in the terminal via command `sudachipy`.
`sudachipy` has 3 subcommands (in default `tokenize`)

```bash
$ sudachipy tokenize -h
usage: sudachipy tokenize [-h] [-r file] [-m {A,B,C}] [-o file] [-a] [-d]
                          file [file ...]

Tokenize Text

positional arguments:
  file        text written in utf-8

optional arguments:
  -h, --help  show this help message and exit
  -r file     the setting file in JSON format
  -m {A,B,C}  the mode of splitting
  -o file     the output file
  -a          print all of the fields
  -d          print the debug information
```
```bash
$ sudachipy build -h
usage: sudachipy build [-h] [-o file] [-d string] -m file file [file ...]

Build Sudachi Dictionary

positional arguments:
  file        source files with CSV format (one of more)

optional arguments:
  -h, --help  show this help message and exit
  -o file     output file (default: system.dic)
  -d string   description comment to be embedded on dictionary

required named arguments:
  -m file     connection matrix file with MeCab's matrix.def format
```
```bash
$ sudachipy ubuild -h
usage: sudachipy ubuild [-h] [-d string] [-o file] [-s file] file [file ...]

Build User Dictionary

positional arguments:
  file        source files with CSV format (one or more)

optional arguments:
  -h, --help  show this help message and exit
  -d string   description comment to be embedded on dictionary
  -o file     output file (default: user.dic)
  -s file     system dictionary (default: ${SUDACHIPY}/resouces/system.dic)
```

### As a Python package

Here is an example usage;

```python
from sudachipy import tokenizer
from sudachipy import dictionary


tokenizer_obj = dictionary.Dictionary().create()


# Multi-granular tokenization
# (following results are w/ `system_full.dic`
# you may not be able to replicate this particular example w/ `system_core.dic`)

mode = tokenizer.Tokenizer.SplitMode.C
[m.surface() for m in tokenizer_obj.tokenize("医薬品安全管理責任者", mode)]
# => ['医薬品安全管理責任者']

mode = tokenizer.Tokenizer.SplitMode.B
[m.surface() for m in tokenizer_obj.tokenize("医薬品安全管理責任者", mode)]
# => ['医薬品', '安全', '管理', '責任者']

mode = tokenizer.Tokenizer.SplitMode.A
[m.surface() for m in tokenizer_obj.tokenize("医薬品安全管理責任者", mode)]
# => ['医薬', '品', '安全', '管理', '責任', '者']


# Morpheme information

m = tokenizer_obj.tokenize("食べ", mode)[0]

m.surface() # => '食べ'
m.dictionary_form() # => '食べる'
m.reading_form() # => 'タベ'
m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']


# Normalization

tokenizer_obj.tokenize("附属", mode)[0].normalized_form()
# => '付属'
tokenizer_obj.tokenize("SUMMER", mode)[0].normalized_form()
# => 'サマー'
tokenizer_obj.tokenize("シュミレーション", mode)[0].normalized_form()
# => 'シミュレーション'
```

## For developer

### Code format

You can use `./scripts/format.sh` and check if your code is in rule. `flake8` `flake8-import-order` `flake8-buitins` is required. See `requirements.txt`

### Test

You can use `./script/test.sh` and check if not your change cause regression.
