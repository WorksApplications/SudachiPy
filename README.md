# SudachiPy

SudachiPy is a Python version of [Sudachi](https://github.com/WorksApplications/Sudachi), a Japanese morphological analyzer.

Sudachi & SudachiPy are developed in [WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/), an institute under [Works Applications](http://www.worksap.com/) that focuses on Natural Language Processing (NLP).

**Warning: SudachiPy is still under development, and some of the functions are still not complete. Please use it at your own risk.**


## Setup

SudachiPy requires Python3.5+.

As SudachiPy is currently under development, it is not registered to PyPI just yet. You may install the package using following `pip` command at the moment.

```
$ pip install -e git+git://github.com/WorksApplications/SudachiPy@develop#egg=SudachiPy
```

or, you can clone and install as per following example.

```bash
$ git clone https://github.com/WorksApplications/SudachiPy.git
$ cd SudachiPy
$ pip install -e .
```

### Dictionary

The dictionary file stored in Git LFS is not the full dictionary. For full dictionary or other dictionary models please see [Releases · WorksApplications/Sudachi](https://github.com/WorksApplications/Sudachi/releases).

Currently, dictionary **must** be located on `<repodir>/resources/system.dic`. When you are changing the model, you may do as per following example. Following example will download, unpack, delete current dictionary if any, and finally rename the newly downloaded dictionary.

```bash
$ cd resources
$ wget https://github.com/WorksApplications/Sudachi/releases/download/v0.1.0/sudachi-0.1.0-dictionary-core.zip && unzip sudachi-0.1.0-dictionary-core.zip
$ ls | grep -e "^system.dic$" | xargs rm -f
$ mv system_core.dic system.dic
```

**Note**: if you use virtual environment and pip installation from git, `<repodir>` is `<virtual_env_dir>/src/sudachipy`

## Usage

### Command Line Interface

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

### Python Package

Here is an example usage;

```python
import json

from sudachipy import tokenizer
from sudachipy import dictionary
from sudachipy import config

with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
    settings = json.load(f)
tokenizer_obj = dictionary.Dictionary(settings).create()


# Multi-granular tokenization
# (following results are w/ `system_full.dic`
# you may not be able to replicate this particular example w/ `system_core.dic`)


mode = tokenizer.Tokenizer.SplitMode.C
[m.surface() for m in tokenizer_obj.tokenize(mode, "医薬品安全管理責任者")]
# => ['医薬品安全管理責任者']

mode = tokenizer.Tokenizer.SplitMode.B
[m.surface() for m in tokenizer_obj.tokenize(mode, "医薬品安全管理責任者")]
# => ['医薬品', '安全', '管理', '責任者']

mode = tokenizer.Tokenizer.SplitMode.A
[m.surface() for m in tokenizer_obj.tokenize(mode, "医薬品安全管理責任者")]
# => ['医薬', '品', '安全', '管理', '責任', '者']


# Morpheme information

m = tokenizer_obj.tokenize(mode, "食べ")[0]

m.surface() # => '食べ'
m.dictionary_form() # => '食べる'
m.reading_form() # => 'タベ'
m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']


# Normalization

tokenizer_obj.tokenize(mode, "附属")[0].normalized_form()
# => '付属'
tokenizer_obj.tokenize(mode, "SUMMER")[0].normalized_form()
# => 'サマー'
tokenizer_obj.tokenize(mode, "シュミレーション")[0].normalized_form()
# => 'シミュレーション'
```
