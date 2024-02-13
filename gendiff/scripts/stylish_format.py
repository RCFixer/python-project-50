
def convert_values(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


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
