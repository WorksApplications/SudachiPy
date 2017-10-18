import sys
import json
import argparse

from sudachi import config
from sudachi import dictionaryfactory
from sudachi import tokenizer


def run(tokenizer, mode, reader, output, print_all):
    for line in reader.readlines():
        for m in tokenizer.tokenize(mode, line):
            print(m.surface(), file=output, end='')
            print("\t", file=output, end='')
            print(','.join(m.part_of_speech()), file=output, end='')
            print("\t", file=output, end='')
            print(m.normalized_form(), file=output, end='')
            if print_all:
                print("\t", file=output, end='')
                print(m.dictionary_form(), file=output, end='')
                print("\t", file=output, end='')
                print(m.reading_form(), file=output, end='')
                if m.is_oov():
                    print("\t", file=output, end='')
                    print("(OOV)", file=output, end='')
            print("", file=output)
        print("EOS", file=output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Japanese Morphological Analyzer")
    parser.add_argument("-r", dest="fpath_setting", metavar="file",
                        default=config.SETTINGFILE, help="the setting file in JSON format")
    parser.add_argument("-m", dest="mode", choices=["A", "B", "C"], default="C", help="the mode of splitting")
    parser.add_argument("-o", dest="fpath_out", metavar="file", help="the output file")
    parser.add_argument("-a", action="store_true", help="print all of the fields")
    parser.add_argument("-d", action="store_true", help="print the debug information")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("input_files", metavar="input file(s)", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    with open(args.fpath_setting, "r", encoding="utf-8") as f:
        settings = json.load(f)

    if args.mode == "A":
        mode = tokenizer.Tokenizer.SplitMode.A
    elif args.mode == "B":
        mode = tokenizer.Tokenizer.SplitMode.B
    else:
        mode = tokenizer.Tokenizer.SplitMode.C

    output = sys.stdout
    if args.fpath_out:
        output = open(args.fpath_out, "w", encoding="utf-8")

    print_all = args.a

    is_enable_dump = args.d

    dict_ = dictionaryfactory.DictionaryFactory().create(settings)
    tokenizer = dict_.create()
    if is_enable_dump:
        tokenizer.set_dump_output(output)

    input_files = args.input_files
    if input_files:
        for input_file in input_files:
            with open(input_file, "r", encoding="utf-8") as input_:
                run(tokenizer, mode, input_, output, print_all)
    else:
        run(tokenizer, mode, sys.stdin, output, print_all)

    output.close()
