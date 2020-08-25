# SudachiPy
[![PyPi version](https://img.shields.io/pypi/v/sudachipy.svg)](https://pypi.python.org/pypi/sudachipy/)
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Build Status](https://travis-ci.com/WorksApplications/SudachiPy.svg?branch=develop)](https://travis-ci.com/WorksApplications/SudachiPy)
[![](https://img.shields.io/github/license/WorksApplications/SudachiPy.svg)](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)

SudachiPy is a Python version of [Sudachi](https://github.com/WorksApplications/Sudachi), a Japanese morphological analyzer.


## TL;DR

```bash
$ pip install sudachipy sudachidict_core

$ echo "高輪ゲートウェイ駅" | sudachipy
高輪ゲートウェイ駅	名詞,固有名詞,一般,*,*,*	高輪ゲートウェイ駅
EOS

$ echo "高輪ゲートウェイ駅" | sudachipy -m A
高輪	名詞,固有名詞,地名,一般,*,*	高輪
ゲートウェイ	名詞,普通名詞,一般,*,*,*	ゲートウェー
駅	名詞,普通名詞,一般,*,*,*	駅
EOS

$ echo "空缶空罐空きカン" | sudachipy -a
空缶	名詞,普通名詞,一般,*,*,*	空き缶	空缶	アキカン	0
空罐	名詞,普通名詞,一般,*,*,*	空き缶	空罐	アキカン	0
空きカン	名詞,普通名詞,一般,*,*,*	空き缶	空きカン	アキカン	0
EOS
```

## Setup

You need SudachiPy and a dictionary.

### Step 1. Install SudachiPy

```bash
$ pip install sudachipy
```

### Step 2. Get a Dictionary

You can get dictionary as a Python package. It make take a while to download the dictionary file (around 70MB for the `core` edition).

```bash
$ pip install sudachidict_core
```

Alternatively, you can choose other dictionary editions. See [this section](#dictionary-edition) for the detail.


## Usage: As a command

There is a CLI command `sudachipy`.

```bash
$ echo "外国人参政権" | sudachipy
外国人参政権	名詞,普通名詞,一般,*,*,*	外国人参政権
EOS
$ echo "外国人参政権" | sudachipy -m A
外国	名詞,普通名詞,一般,*,*,*	外国
人	接尾辞,名詞的,一般,*,*,*	人
参政	名詞,普通名詞,一般,*,*,*	参政
権	接尾辞,名詞的,一般,*,*,*	権
EOS
```

```bash
$ sudachipy tokenize -h
usage: sudachipy tokenize [-h] [-r file] [-m {A,B,C}] [-o file] [-a] [-d] [-v]
                          [file [file ...]]

Tokenize Text

positional arguments:
  file           text written in utf-8

optional arguments:
  -h, --help     show this help message and exit
  -r file        the setting file in JSON format
  -m {A,B,C}     the mode of splitting
  -o file        the output file
  -a             print all of the fields
  -d             print the debug information
  -v, --version  print sudachipy version
```

### Output

Columns are tab separated.

- Surface
- Part-of-Speech Tags (comma separated)
- Normalized Form

When you add the `-a` option, it additionally outputs

- Dictionary Form
- Reading Form
- Dictionary ID
  - `0` for the system dictionary
  - `1` and above for the [user dictionaries](#user-dictionary)
  - `-1\t(OOV)` if a word is Out-of-Vocabulary (not in the dictionary)

```bash
$ echo "外国人参政権" | sudachipy -a
外国人参政権	名詞,普通名詞,一般,*,*,*	外国人参政権	外国人参政権	ガイコクジンサンセイケン	0
EOS
```

```bash
echo "阿quei" | sudachipy -a
阿	名詞,普通名詞,一般,*,*,*	阿	阿		-1	(OOV)
quei	名詞,普通名詞,一般,*,*,*	quei	quei		-1	(OOV)
EOS
```


## Usage: As a Python package

Here is an example;

```python
from sudachipy import tokenizer
from sudachipy import dictionary

tokenizer_obj = dictionary.Dictionary().create()
```

```python
# Multi-granular Tokenization

mode = tokenizer.Tokenizer.SplitMode.C
[m.surface() for m in tokenizer_obj.tokenize("国家公務員", mode)]
# => ['国家公務員']

mode = tokenizer.Tokenizer.SplitMode.B
[m.surface() for m in tokenizer_obj.tokenize("国家公務員", mode)]
# => ['国家', '公務員']

mode = tokenizer.Tokenizer.SplitMode.A
[m.surface() for m in tokenizer_obj.tokenize("国家公務員", mode)]
# => ['国家', '公務', '員']
```


```python
# Morpheme information

m = tokenizer_obj.tokenize("食べ", mode)[0]

m.surface() # => '食べ'
m.dictionary_form() # => '食べる'
m.reading_form() # => 'タベ'
m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']
```


```python
# Normalization

tokenizer_obj.tokenize("附属", mode)[0].normalized_form()
# => '付属'
tokenizer_obj.tokenize("SUMMER", mode)[0].normalized_form()
# => 'サマー'
tokenizer_obj.tokenize("シュミレーション", mode)[0].normalized_form()
# => 'シミュレーション'
```

(With `20200330` `core` dictionary. The results may change when you use other versions)


## Dictionary Edition

There are three editions of Sudachi Dictionary, namely, `small`, `core`, and `full`. See [WorksApplications/SudachiDict](https://github.com/WorksApplications/SudachiDict) for the detail.

SudachiPy uses `sudachidict_core` by default. You can specify the dictionary with the `link -t` command.

```bash
$ pip install sudachidict_small
$ sudachipy link -t small
```

```bash
$ pip install sudachidict_full
$ sudachipy link -t full
```

You can remove the dictionary link with the `link -u` commnad.

```bash
$ sudachipy link -u
```

Dictionaries are installed as Python packages `sudachidict_small`, `sudachidict_core`, and `sudachidict_full`. SudachiPy tries to refer `sudachidict` package to use a dictionary. The `link` subcommand creates *a symbolic link* of `sudachidict_*` as `sudachidict`, to switch the packages.

* [SudachiDict-small · PyPI](https://pypi.org/project/SudachiDict-small/)
* [SudachiDict-core · PyPI](https://pypi.org/project/SudachiDict-core/)
* [SudachiDict-full · PyPI](https://pypi.org/project/SudachiDict-full/)

The dictionary files are not in the package itself, but it is downloaded upon installation.

### Dictionary in The Setting File

Alternatively, if the dictionary file is specified in the setting file, `sudachi.json`, SudachiPy will use that file.

```
{
    "systemDict" : "relative/path/to/system.dic",
    ...
}
```

The default setting file is [sudachipy/resources/sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json). You can specify your `sudachi.json` with the `-r` option.

```bash
$ sudachipy -r path/to/sudachi.json
``` 


## User Dictionary

To use a user dictionary, `user.dic`, place [sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json) to anywhere you like, and add `userDict` value with the relative path from `sudachi.json` to your `user.dic`.

```js
{
    "userDict" : ["relative/path/to/user.dic"],
    ...
}
```

Then specify your `sudachi.json` with the `-r` option.

```bash
$ sudachipy -r path/to/sudachi.json
``` 


You can build a user dictionary with the subcommand `ubuild`.  

**WARNING: v0.3.\* ubuild contains bug.**

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
  -s file     system dictionary (default: linked system_dic, see link -h)
```

About the dictionary file format, please refer to [this document](https://github.com/WorksApplications/Sudachi/blob/develop/docs/user_dict.md) (written in Japanese, English version is not available yet).


## Customized System Dictionary

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

To use your customized `system.dic`, place [sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json) to anywhere you like, and overwrite `systemDict` value with the relative path from `sudachi.json` to your `system.dic`.

```
{
    "systemDict" : "relative/path/to/system.dic",
    ...
}
```

Then specify your `sudachi.json` with the `-r` option.

```bash
$ sudachipy -r path/to/sudachi.json
``` 


## For Developers

### Cython Build

```sh
$ python setup.py build_ext --inplace
```

### Code Format

Run `scripts/format.sh` to check if your code is formatted correctly.

You need packages `flake8` `flake8-import-order` `flake8-buitins` (See `requirements.txt`).

### Test

Run `scripts/test.sh` to run the tests.


## Contact

Sudachi and SudachiPy are developed by [WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/).

Open an issue, or come to our Slack workspace for questions and discussion.

https://sudachi-dev.slack.com/ (Get invitation [here](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU))

Enjoy tokenization!
