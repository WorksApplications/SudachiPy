from sudachipy import config
from sudachipy import dictionary
from sudachipy.morphemelist import MorphemeList
import json

EXAMPLE_SENTENCE = "スダチ（酢橘、学名:Citrus sudachi）はミカン科の常緑低木ないし中高木。徳島県原産の果物で、カボスやユコウと同じ香酸柑橘類。"

with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
    settings = json.load(f)

tokenizer_obj = dictionary.Dictionary(settings).create()
mode = tokenizer_obj.SplitMode.B
morpheme_list = tokenizer_obj.tokenize(mode, EXAMPLE_SENTENCE)  # type: MorphemeList

for m in morpheme_list:
    list_info = [
        m.surface(),
        ",".join(m.part_of_speech()),
        m.normalized_form()]
    print("\t".join(list_info))
print("EOS")