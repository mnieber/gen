import inflect

p = inflect.engine()


def plural(x):
    return p.plural_noun(x) or x


def singular(x):
    return p.singular_noun(x) or x
