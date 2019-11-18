# 日本語形態素解析器 SudachiPy（[Sudachi](https://github.com/WorksApplications/Sudachi/) Pythonクローン） チュートリアル

pip をつかってインストールします。Python 3.5以上が必要です。 

```
$ pip install -e git+git://github.com/WorksApplications/SudachiPy@develop#egg=SudachiPy
```

パッケージには辞書が含まれていません。Java版をビルドして target/system_*.dic を取得するか、[リリース一覧](https://github.com/WorksApplications/Sudachi/releases)から辞書を取得します。 

```
$ wget https://github.com/WorksApplications/Sudachi/releases/download/v0.1.1/sudachi-0.1.1-dictionary-core.zip
$ unzip sudachi-0.1.1-dictionary-core.zip
$ cp system_core.dic `pip show sudachipy | grep Location | sed 's/^.*: //'`/resources/system.dic
```

コマンドラインツールの利用方法は[Java版](https://github.com/WorksApplications/Sudachi/blob/develop/docs/tutorial.md)とほぼ同じです。 

```
$ sudachipy
きょうはいい天気ですね。
きょう  名詞,普通名詞,副詞可能,*,*,*    今日
は      助詞,係助詞,*,*,*,*     は
いい    形容詞,非自立可能,*,*,形容詞,連体形-一般        良い
天気    名詞,普通名詞,一般,*,*,*        天気
です    助動詞,*,*,*,助動詞-デス,終止形-一般    です
ね      助詞,終助詞,*,*,*,*     ね
。      補助記号,句点,*,*,*,*   。
EOS
```
