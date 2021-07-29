def lower0(x):
    return x[0].lower() + x[1:]


def upper0(x):
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


def kebab_to_snake(x):
    return x.replace("-", "_")


def snake_to_kebab(x):
    return x.replace("_", "-")


def snake_to_camel(x):
    components = x.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
