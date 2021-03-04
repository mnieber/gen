def title0(x):
    return x[0].upper() + x[1:]


def kebab_to_camel(x):
    result = ""
    transform = False
    for char in x:
        if char == "-":
            transform = True
        elif transform:
            result += char.upper()
            transform = False
        else:
            result += char

    return result
