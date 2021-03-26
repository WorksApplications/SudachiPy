# 日本語形態素解析器 SudachiPy チュートリアル
[![PyPi version](https://img.shields.io/pypi/v/sudachipy.svg)](https://pypi.python.org/pypi/sudachipy/)
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Build Status](https://travis-ci.com/WorksApplications/SudachiPy.svg?branch=develop)](https://travis-ci.com/WorksApplications/SudachiPy)
[![](https://img.shields.io/github/license/WorksApplications/SudachiPy.svg)](https://github.com/WorksApplications/SudachiPy/blob/develop/LICENSE)

SudachiPyは日本語形態素解析器[Sudachi](https://github.com/WorksApplications/Sudachi)のpython版です。


## とりあえず動かしたい場合

```
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

## 導入

SudachiPyを使う場合は辞書が必要になります。
※パッケージには辞書が含まれていません。

### Step 1. SudachiPyのインストール

```bash
$ pip install sudachipy
```

### Step 2. 辞書のインストール

辞書はPythonのパッケージとしてダウンロードできます。

※辞書のダウンロードは時間がかかります (`core`辞書は約70MB ).

```bash
$ pip install sudachidict_core
```

また、他の辞書を選択することもできます。詳細は[このセッション](#辞書の種類)を参照してください。


## 使用方法（CLI）
CLIでは以下のように実行できます。

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
usage: sudachipy tokenize [-h] [-r file] [-m {A,B,C}] [-o file] [-s string]
                          [-a] [-d] [-v]
                          [file [file ...]]

Tokenize Text

positional arguments:
  file           text written in utf-8

optional arguments:
  -h, --help     show this help message and exit
  -r file        the setting file in JSON format
  -m {A,B,C}     the mode of splitting
  -o file        the output file
  -s string      sudachidict type
  -a             print all of the fields
  -d             print the debug information
  -v, --version  print sudachipy version
```

### 出力形式
タブ区切りで出力されます。
デフォルトは以下の情報が含まれます。

- 表層形
- 品詞（コンマ区切り）
- 正規化表記

オプションで `-a` を指定すると以下の情報が追加されます。

- 辞書形
- 読み
- 辞書ID
  - `0` システム辞書
  - `1` ユーザー辞書
  - `-1\t(OOV)` 未知語（辞書に含まれない単語）

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

## 使用方法(Python パッケージ)

例 

```python
from sudachipy import tokenizer
from sudachipy import dictionary

tokenizer_obj = dictionary.Dictionary().create()
```

```python
# 複数粒度分割

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
# 形態素情報

m = tokenizer_obj.tokenize("食べ", mode)[0]

m.surface() # => '食べ'
m.dictionary_form() # => '食べる'
m.reading_form() # => 'タベ'
m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']
```

```python
# 正規化

tokenizer_obj.tokenize("附属", mode)[0].normalized_form()
# => '付属'
tokenizer_obj.tokenize("SUMMER", mode)[0].normalized_form()
# => 'サマー'
tokenizer_obj.tokenize("シュミレーション", mode)[0].normalized_form()
# => 'シミュレーション'
```

(これは `20200330` `core` 辞書による出力例です。 辞書のバージョンによって変わる可能性があります。)

## 辞書の種類

**WARNING: `sudachipy link` コマンドは SudachiPy v0.5.2 以降から利用できなくなりました. **

Sudachi辞書は`small`と`core`と`full`の3種類があります。 詳細は[WorksApplications/SudachiDict](https://github.com/WorksApplications/SudachiDict)を参照してください。

SudachiPyはデフォルトでは`sudachidict_core`に設定されています。

`sudachidict_small`, `sudachidict_core`, `sudachidict_full`はPythonのパッケージとしてインストールされます。

* [SudachiDict-small · PyPI](https://pypi.org/project/SudachiDict-small/)
* [SudachiDict-core · PyPI](https://pypi.org/project/SudachiDict-core/)
* [SudachiDict-full · PyPI](https://pypi.org/project/SudachiDict-full/)

辞書ファイルはパッケージ自体には含まれていませんが、上記のインストール時にダウンロードする処理が埋め込まれています。

### 辞書オプション: コマンドライン

辞書設定の変更は`-s`オプションで指定することができます。


```bash
$ pip install sudachidict_small
$ echo "外国人参政権" | sudachipy -s small
```

```bash
$ pip install sudachidict_full
$ echo "外国人参政権" | sudachipy -s full
```

### 辞書オプション: Python パッケージ

Dictionary の引数 `config_path` または `dict_type` から利用する辞書を指定することができます。

```python
class Dictionary(config_path=None, resource_dir=None, dict_type=None)
```

1. `config_path`
    * `config_path` で辞書の設定ファイルのパスを指定することができます（[辞書の設定ファイル](#辞書の設定ファイル) 参照）。
    * 指定した辞書の設定ファイルに、辞書のファイルパス `systemDict` が記述されていれば、その辞書を優先して利用します．
2. `dict_type`
    * `dict_type` オプションで辞書の種類を直接指定することもできます。
    * `small`, `core`, `full` の３種類が指定可能です。
    * `config_path` と `dict_type` で異なる辞書が指定されている場合、**`dict_type` が優先**されます。 

```python
from sudachipy import tokenizer
from sudachipy import dictionary

# デフォルトは sudachidict_core が設定されている
tokenizer_obj = dictionary.Dictionary().create()  

# /path/to/sudachi.json の systemDict で指定されている辞書が設定される
tokenizer_obj = dictionary.Dictionary(config_path="/path/to/sudachi.json").create()  

# dict_type で指定された辞書が設定される
tokenizer_obj = dictionary.Dictionary(dict_type="core").create()  # sudachidict_core （デフォルトと同じ）
tokenizer_obj = dictionary.Dictionary(dict_type="small").create()  # sudachidict_small
tokenizer_obj = dictionary.Dictionary(dict_type="full").create()  # sudachidict_full

# dict_type (sudachidict_full) が優先される
tokenizer_obj = dictionary.Dictionary(config_path="/path/to/sudachi.json", dict_type="full").create()  
```


### 辞書の設定ファイル

また、`sudachi.json`で辞書ファイルを切り替えることができます。

辞書のファイルパス `systemDict` は、絶対パスと相対パスのどちらでも指定可能です。

相対パスは、辞書の設定ファイルからの相対パスです。


```
{
    "systemDict" : "relative/path/to/system.dic",
    ...
}
```

デフォルトは[sudachipy/resources/sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json)を参照します。 `sudachi.json`を新たに用意する場合は `-r`で指定してください.

```bash
$ sudachipy -r path/to/sudachi.json
``` 

## ユーザー辞書
ユーザー辞書`user.dic`を使用する場合は、[sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json)を好きな場所に配置し、`sudachi.json`から`user.dic`への相対パスをuserDictの値に追加してください。

```js
{
    "userDict" : ["relative/path/to/user.dic"],
    ...
}
```

そして、その `sudachi.json`を`-r`で指定します。

```bash
$ sudachipy -r path/to/sudachi.json
``` 

サブコマンド`ubuild`によってユーザー辞書を作成できます。

**WARNING: v0.3.\* ubuildはバグを含んでいます**

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
  -s file     system dictionary path (default: system core dictionary path)
```

辞書ファイル形式については[user_dict.md](https://github.com/WorksApplications/Sudachi/blob/develop/docs/user_dict.md)を参照してください。 


## システム辞書のカスタマイズ

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

カスタマイズしたシステム辞書`system.dic`を使用する場合は、[sudachi.json](https://github.com/WorksApplications/SudachiPy/blob/develop/sudachipy/resources/sudachi.json)を好きな場所に配置し、`sudachi.json`から`system.dic`への相対パスでsystemDictの値を上書きしてください。

```
{
    "systemDict" : "relative/path/to/system.dic",
    ...
}
```

そして、その `sudachi.json`を`-r`で指定します。

```bash
$ sudachipy -r path/to/sudachi.json
``` 

## 開発者向け
### Cython Build

```sh
$ python setup.py build_ext --inplace
```

### Code Format

`scripts/format.sh`を実行して、コードが正しいフォーマットかを確認してください。

`flake8` `flake8-import-order` `flake8-buitins`が必要です。 (`requirements.txt`参照).

### Test

`scripts/test.sh`を実行してテストしてください。


## Contact

SudachiとSudachiPyは[WAP Tokushima Laboratory of AI and NLP](http://nlp.worksap.co.jp/)によって開発されています.

開発者やユーザーの方々が質問したり議論するためのSlackワークスペースを用意しています。

- https://sudachi-dev.slack.com/ ([こちら](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU)から招待を受けてください)


