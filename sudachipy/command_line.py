import sys
import json
import argparse

from . import config
from . import dictionary
from . import tokenizer


def run(tokenizer_obj, skip_comments, mode, print_sub_morphemes, reader, output, print_all):
    for line in iter(sys.stdin.readline, ""):
        line = line.rstrip()
        if skip_comments and line.startswith('#'):
            print(line, file=output)
            continue
        for m in tokenizer_obj.tokenize(mode, line):
            if not print_sub_morphemes or mode == tokenizer.Tokenizer.SplitMode.A:
                _print_morpheme(m, output, print_all)
            elif mode is tokenizer.Tokenizer.SplitMode.B:
                _print_morpheme_B(m, output, print_all, "")
            elif mode is tokenizer.Tokenizer.SplitMode.C:
                _print_morpheme_C(m, output, print_all)
        print("EOS", file=output)


def _print_morpheme(m, output, print_all):
    list_info = [
        m.surface(),
        ",".join(m.part_of_speech()),
        m.normalized_form()]
    if print_all:
        list_info += [
            m.dictionary_form(),
            m.reading_form(),
            str(m.dictionary_id())]
        if m.is_oov():
            list_info.append("(OOV)")
    print("\t".join(list_info), file=output)


def _print_morpheme_B(m, output, print_all, prefix):
    morphemes = m.split(tokenizer.Tokenizer.SplitMode.A)
    print(prefix, end="", file=output)
    _print_morpheme(m, output, print_all)
    if len(morphemes) > 1:
        for sub_morpheme in morphemes:
            print("@A ", end="", file=output)
            _print_morpheme(sub_morpheme, output, print_all)


def _print_morpheme_C(m, output, print_all):
    morphemes = m.split(tokenizer.Tokenizer.SplitMode.B)
    if len(morphemes) == 1:
        _print_morpheme_B(m, output, print_all, "")
    else:
        _print_morpheme(m, output, print_all)
        for sub_morpheme in morphemes:
            _print_morpheme_B(sub_morpheme, output, print_all, "@B ")


def main():
    parser = argparse.ArgumentParser(description="Japanese Morphological Analyzer")
    parser.add_argument("-r", dest="fpath_setting", metavar="file",
                        default=config.SETTINGFILE, help="the setting file in JSON format")
    parser.add_argument("-c", action="store_true", help="skip comment lines starting with # (just print them)")
    parser.add_argument("-m", dest="mode", choices=["A", "B", "C"], default="C", help="the mode of splitting")
    parser.add_argument("-s", action="store_true", help="print sub word lines starting with @A or @B")
    parser.add_argument("-o", dest="fpath_out", metavar="file", help="the output file")
    parser.add_argument("-a", action="store_true", help="print all of the fields")
    parser.add_argument("-d", action="store_true", help="print the debug information")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("input_files", metavar="input file(s)", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    with open(args.fpath_setting, "r", encoding="utf-8") as f:
        settings = json.load(f)

    skip_comments = args.c

    if args.mode == "A":
        mode = tokenizer.Tokenizer.SplitMode.A
    elif args.mode == "B":
        mode = tokenizer.Tokenizer.SplitMode.B
    else:
        mode = tokenizer.Tokenizer.SplitMode.C

    print_sub_morphemes = args.s

    output = sys.stdout
    if args.fpath_out:
        output = open(args.fpath_out, "w", encoding="utf-8")

    print_all = args.a

    is_enable_dump = args.d

    dict_ = dictionary.Dictionary(settings)
    tokenizer_obj = dict_.create()
    if is_enable_dump:
        tokenizer_obj.set_dump_output(output)
    input_files = args.input_files
    if input_files:
        for input_file in input_files:
            with open(input_file, "r", encoding="utf-8") as input_:
                run(tokenizer_obj, skip_comments, mode, print_sub_morphemes, input_, output, print_all)
    else:
        run(tokenizer_obj, skip_comments, mode, print_sub_morphemes, sys.stdin, output, print_all)

    output.close()


if __name__ == '__main__':
    main()
