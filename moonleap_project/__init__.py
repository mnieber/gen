import os

from moonleap.parser.term import term_to_word, verb_to_word
from moonleap.utils.case import lower0, upper0
from moonleap.utils.inflect import plural

from . import (
    dockercompose,
    dockercompose_and_project,
    dockercompose_and_service,
    dockerfile,
    project,
    project_and_service,
    service,
    service_and_docker,
    srcdir,
    vscodeproject,
)

modules = [
    (dockercompose),
    (dockercompose_and_project),
    (dockercompose_and_service),
    (dockerfile),
    (project),
    (project_and_service),
    (service),
    (service_and_docker),
    (srcdir),
    (vscodeproject),
]

filters = {
    "plural": lambda x: plural(x),
    "upper0": upper0,
    "term_to_word": lambda x: x if x is None else term_to_word(x),
    "verb_to_word": verb_to_word,
    "lower0": lower0,
    "expand_vars": lambda x: os.path.expandvars(x),
    "dbg": lambda x: __import__("pudb").set_trace(),
}
