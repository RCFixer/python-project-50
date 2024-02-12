import argparse
import yaml

__all__ = ('generate_diff',)


def main():
    parser = argparse.ArgumentParser(description='Compares two '
                                                 'configuration files'
                                                 ' and shows a difference.')
    parser.add_argument('file1', metavar='first_file')
    parser.add_argument('file2', metavar='second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    diff = generate_diff(args.file1, args.file2)
    print(diff)


def convert_values(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def find_diff(file1, file2):
    result = {}
    for key, value in file1.items():
        if key in file2 and file2[key] == value:
            result[('=', key)] = value
        elif key in file2 and file2[key] != value:
            result[('-', key)] = value
            result[('+', key)] = file2[key]
        else:
            result[('-', key)] = value
    for key, value in file2.items():
        if key not in file1:
            result[('+', key)] = value
    return result


def convert_to_string(diff):
    result = []
    for key, value in diff.items():
        match key[0]:
            case '=':
                result.append(f'  {key[1]}: {convert_values(value)}')
            case '-':
                result.append(f'- {key[1]}: {convert_values(value)}')
            case '+':
                result.append(f'+ {key[1]}: {convert_values(value)}')
    return '{\n\t' + '\n\t'.join(result) + '\n}'


def generate_diff(file1_path, file2_path):
    file1 = yaml.load(open(file1_path), Loader=yaml.FullLoader)
    file2 = yaml.load(open(file2_path), Loader=yaml.FullLoader)
    diff = find_diff(file1, file2)
    sorted_diff = dict(sorted(diff.items(),
                              key=lambda item: item[0][1] or item[0][0]))
    result = convert_to_string(sorted_diff)
    return result


if __name__ == '__main__':
    main()
