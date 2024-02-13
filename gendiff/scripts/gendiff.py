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
    elif value is None:
        return 'null'
    return value


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


def stylish(diff, indentation=0):
    result = []
    spaces = (indentation + 1) * '\t'
    for key, value in diff.items():
        match key[0]:
            case '=':
                if isinstance(value, dict):
                    result.append(f'{spaces}  {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces}  {key[1]}: {convert_values(value)}')
            case '-':
                if isinstance(value, dict):
                    result.append(f'{spaces}- {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces}- {key[1]}: {convert_values(value)}')
            case '+':
                if isinstance(value, dict):
                    result.append(f'{spaces}+ {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces}+ {key[1]}: {convert_values(value)}')
            case _:
                if isinstance(value, dict):
                    result.append(f'{spaces}  {key}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces}  {key}: {convert_values(value)}')
    if indentation == 0:
        spaces = ''
    return '{\n' + '\n'.join(result) + '\n' + spaces + '}'


def generate_diff(file1_path, file2_path, formatter=stylish):
    file1 = yaml.load(open(file1_path), Loader=yaml.FullLoader)
    file2 = yaml.load(open(file2_path), Loader=yaml.FullLoader)
    diff = find_diff(file1, file2)
    result = formatter(diff)
    return result


if __name__ == '__main__':
    main()
