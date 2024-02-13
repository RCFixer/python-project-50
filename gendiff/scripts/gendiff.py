import argparse
import yaml

from . stylish_format import stylish
from . plain_format import plain

__all__ = ('generate_diff',)


def main():
    parser = argparse.ArgumentParser(description='Compares two '
                                                 'configuration files'
                                                 ' and shows a difference.')
    parser.add_argument('file1', metavar='first_file')
    parser.add_argument('file2', metavar='second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    style_format = args.format if args.format else 'stylish'
    diff = generate_diff(args.file1, args.file2, style_format)
    if style_format == 'plain':
        for re in diff:
            print(re)
    elif style_format == 'stylish':
        print(diff)


def find_diff(file1, file2):
    result = {}
    for key, value in file1.items():
        if isinstance(value, dict) and key in file2 and isinstance(file2[key], dict):
            result[('=', key)] = find_diff(value, file2[key])
        elif key in file2 and file2[key] == value:
            result[('=', key)] = value
        elif key in file2 and file2[key] != value:
            result[('-', key)] = value
            result[('+', key)] = file2[key]
        else:
            result[('-', key)] = value
    if isinstance(file2, dict):
        for key, value in file2.items():
            if key not in file1:
                result[('+', key)] = value
    sorted_result = dict(sorted(result.items(),
                         key=lambda item: item[0][1] or item[0][0]))
    return sorted_result


def generate_diff(file1_path, file2_path, formatter='stylish'):
    file1 = yaml.load(open(file1_path), Loader=yaml.FullLoader)
    file2 = yaml.load(open(file2_path), Loader=yaml.FullLoader)
    diff = find_diff(file1, file2)
    if formatter == 'plain':
        result = plain(diff)
    else:
        result = stylish(diff)
    return result


if __name__ == '__main__':
    main()
