import argparse
import json

parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
parser.add_argument('file1', metavar='first_file')
parser.add_argument('file2', metavar='second_file')
parser.add_argument('-f', '--format', help='set format of output')
args = parser.parse_args()

__all__ = ('generate_diff',)


def main(file1_path=args.file1, file2_path=args.file2):
    diff = generate_diff(file1_path, file2_path)
    print(diff)


def convert_values(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file1_path, file2_path):
    file1 = json.load(open(file1_path))
    file2 = json.load(open(file2_path))
    diff = {}
    for key, value in file1.items():
        if key in file2 and file2[key] == value:
            diff[('=', key)] = value
        elif key in file2 and file2[key] != value:
            diff[('-', key)] = value
            diff[('+', key)] = file2[key]
        else:
            diff[('-', key)] = value
    for key, value in file2.items():
        if key not in file1:
            diff[('+', key)] = value
    sorted_diff = dict(sorted(diff.items(), key=lambda item: item[0][1] or item[0][0]))
    result = []
    for key, value in sorted_diff.items():
        match key[0]:
            case '=':
                result.append(f'  {key[1]}: {convert_values(value)}')
            case '-':
                result.append(f'- {key[1]}: {convert_values(value)}')
            case '+':
                result.append(f'+ {key[1]}: {convert_values(value)}')
    return '{\n\t' + '\n\t'.join(result) + '\n}'


if __name__ == '__main__':
    main(args.file1, args.file2)
