import re


def l0(x):
    return x[0].lower() + x[1:] if x else x


def u0(x):
    return x[0].upper() + x[1:] if x else x


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


def camel_to_kebab(x):
    return snake_to_kebab(camel_to_snake(x))


def snake_to_camel(x):
    components = x.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


_underscorer1 = re.compile(r"(.)([A-Z][a-z]+)")
_underscorer2 = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(s):
    subbed = _underscorer1.sub(r"\1_\2", s)
    return _underscorer2.sub(r"\1_\2", subbed).lower()


def camel_join(lhs, rhs):
    if not lhs:
        return rhs
    return f"{lhs}{u0(rhs)}"


sn = camel_to_snake
