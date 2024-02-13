
def convert_plain_values(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    return value


def plain(diff, path=''):
    result = []
    for key, value in diff.items():
        match key[0]:
            case '=':
                if isinstance(value, dict):
                    result.extend(plain(value, path + key[1] + '.'))
            case '-':
                if ('+', key[1]) in diff:
                    result.append(f"Property '{path + key[1]}' was updated."
                                  f" From {convert_plain_values(value)} to {convert_plain_values(diff[('+', key[1])])}")
                else:
                    result.append(f"Property '{path + key[1]}' was removed")
            case '+':
                if ('-', key[1]) in diff:
                    continue
                result.append(f"Property '{path + key[1]}' was added with value: {convert_plain_values(value)}")
    return result
