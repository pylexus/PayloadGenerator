# модуль argparse: https://jenyay.net/Programming/Argparse
# find in list: https://stackoverflow.com/questions/9542738/python-find-in-list
# Функция reduce: https://datagy.io/python-reduce/


import sys
import argparse
import timeit
import logging
# import functools
from functools import reduce

def createParser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--size')
    arg_parser.add_argument('-i', '--input')
    arg_parser.add_argument('-o', '--output', default='outputData.txt')

    return arg_parser


# def utf8len(s):
    # ToDo: Определить как подсчитывать размер данных с учетом спец. символов
    # return len(s.encode('utf-8')) + 1
    # return sys.getsizeof(s)


def getBlockSize(items: list, begin_index: int, end_index: int) -> int:
    return reduce(lambda v, s: v + len(s.encode('utf-8')) + 1, items[begin_index:end_index], 0)

    # block_size = 0
    # for i in range(begin_index, end_index):
    #     block_size += utf8len(items[i])
    #
    # return block_size


if __name__ == '__main__':
    # s = "qwertyuiop\n"
    # print("s:", s)
    # print("len(s):", len(s))
    # print("len(s.encode('utf16')):", len(s.encode('utf16')))
    #

    startTime = timeit.default_timer()

    # print(__debug__)
    # print(sys.gettrace())

    parser = createParser()
    params = parser.parse_args(sys.argv[1:])

    # Debug mode
    # params.size = 1024
    # params.input = 'test_template.tpl'
    # params.output = 'out_test_template.dat'

    # if str(params.input) == 'None':
    if str(params.input) != 'None':
        requared_size = int(params.size)

        with open(file=params.input, mode='r', encoding='utf-8') as in_file, open(params.output, 'w', encoding='utf-8') as out_file:
            rows = in_file.readlines()
            print(rows)
            start_index = rows.index('{{begin_block}}\n')
            end_index = rows.index('{{end_block}}\n') + 1

            # current_size = len(rows) - 2
            current_size = getBlockSize(rows, 0, start_index)
            current_size += getBlockSize(rows, end_index, len(rows))

            # header
            for i in range(start_index):
                out_file.write(rows[i])

            # body
            body_size = getBlockSize(rows, start_index + 1, end_index - 1)
            while current_size + body_size <= requared_size:
                current_size += body_size
                for i in range(start_index + 1, end_index - 1):
                    out_file.write(rows[i])

            # footer
            for i in range(end_index, len(rows)):
                out_file.write(rows[i])

    endTime = timeit.default_timer()
    print('Execution time:', endTime - startTime)
