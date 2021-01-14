import inflect

p = inflect.engine()


def plural_noun(x):
    return p.plural_noun(x)


def singular_noun(x):
    return p.singular_noun(x)