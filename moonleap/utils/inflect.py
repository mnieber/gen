from moonleap.utils.case import l0, u0

import inflect

p = inflect.engine()

_lut_plural = {}
_lut_singular = {}


def plural(x):
    if x[0].isupper():
        return u0(plural(l0(x)))
    return _lut_plural.get(x, p.plural_noun(x) or x)


def singular(x):
    return _lut_singular.get(x, p.singular_noun(x) or x)


def install_plural(one, many):
    _lut_plural[one] = many
    _lut_singular[many] = one
