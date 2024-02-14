
def convert_values(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def stylish(diff, indentation=0):
    result = []
    spaces = (indentation + 1) * 4 * ' '
    final_spaces = spaces
    for key, value in diff.items():
        match key[0]:
            case '=':
                if isinstance(value, dict):
                    result.append(f'{spaces[2:]}  {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces[2:]}  {key[1]}: {convert_values(value)}')
                final_spaces = spaces[4:]
            case '-':
                if isinstance(value, dict):
                    result.append(f'{spaces[2:]}- {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces[2:]}- {key[1]}: {convert_values(value)}')
                final_spaces = spaces[6:]
            case '+':
                if isinstance(value, dict):
                    result.append(f'{spaces[2:]}+ {key[1]}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces[2:]}+ {key[1]}: {convert_values(value)}')
                final_spaces = spaces[4:]
            case _:
                if isinstance(value, dict):
                    result.append(f'{spaces}{key}: {stylish(value, indentation + 1)}')
                else:
                    result.append(f'{spaces}{key}: {convert_values(value)}')
                final_spaces = spaces[4:]
    if indentation == 0:
        final_spaces = ''
    return '{\n' + '\n'.join(result) + '\n' + final_spaces + '}'
