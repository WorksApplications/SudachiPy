import json
import sys

from sudachi import config
from sudachi import dictionaryfactory
from sudachi import tokenizer


argvs = sys.argv
argc = len(argvs)


def run(tokenizer, mode, reader, output, print_all):
    for line in reader.readlines():
        print(line)
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
            print("", file=output, end='')
        print("EOS", file=output)






if __name__ == "__main__":
    mode = tokenizer.Tokenizer.SplitMode.C
    settings = None
    output = sys.stdout
    is_enable_dump = False
    print_all = False

    n = 1
    while n < argc:
        if argvs[n] is "-r" and n + 1 < argc:
            n += 1
            with open(argvs[n], 'r') as input_:
                settings = input_.read()

        elif argvs[n] is "-m" and n + 1 < argc:
            n += 1
            if argvs[n] is "A":
                mode = tokenizer.Tokenizer.SplitMode.A
            elif argvs[n] is "B":
                mode = tokenizer.Tokenizer.SplitMode.B
            else:
                mode = tokenizer.Tokenizer.SplitMode.C
        elif argvs[n] is "-o" and n + 1 < argc:
            n += 1
            output = open(argvs[n], 'w')
        elif argvs[n] is "-a":
            print_all = True
        elif argvs[n] is "-d":
            is_enable_dump = True
        elif argvs[n] is "-h":
            print("usage: SudachiCommandLine [-r file] [-m A|B|C] [-o file] [-d] [file ...]", file=sys.stderr)
            print("\t-r file\tread settings from file", file=sys.stderr)
            print("\t-m mode\tmode of splitting", file=sys.stderr)
            print("\t-o file\toutput to file", file=sys.stderr)
            print("\t-a\tprint all fields", file=sys.stderr)
            print("\t-d\tdebug mode", file=sys.stderr)
            exit(1)
        else:
            break
        n += 1

    if settings is None:
        with open(config.SETTINGFILE, 'r') as input_:
            settings = json.load(input_)

    dict_ = dictionaryfactory.DictionaryFactory().create(settings)
    tokenizer = dict_.create()
    if is_enable_dump:
        tokenizer.set_dump_output(output)

    if (n < argc):
        while n < argc:
            with open(argvs[n], 'r') as input_:
                run(tokenizer, mode, input_, output, print_all)
            n += 1
    else:
        run(tokenizer, mode, sys.stdin, output, print_all)
    output.close()
