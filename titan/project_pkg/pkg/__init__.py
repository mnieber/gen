import os

from moonleap.parser.term import term_to_word, verb_to_word
from moonleap.utils.case import l0, u0
from moonleap.utils.inflect import plural

filters = {
    "plural": lambda x: plural(x),
    "u0": u0,
    "term_to_word": lambda x: x if x is None else term_to_word(x),
    "verb_to_word": verb_to_word,
    "l0": l0,
    "expand_vars": lambda x: os.path.expandvars(x),
    "dbg": lambda x: __import__("pudb").set_trace(),
}
