import io
import json
import os

from moonleap.parser.term import verb_to_word
from moonleap.utils.case import l0, u0
from moonleap.utils.inflect import plural
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=2, offset=2)


def sort_dict(item: dict):
    return {
        k: sort_dict(v) if isinstance(v, dict) else v for k, v in sorted(item.items())
    }


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=2, separators=(",", ": "))


def to_nice_yaml(value):
    with io.StringIO() as f:
        yaml.dump(sort_dict(value), stream=f)
        return f.getvalue()


filters = {
    "plural": lambda x: plural(x),
    "u0": u0,
    "to_str": lambda x: x if x is None else str(x),
    "to_nice_json": to_nice_json,
    "to_nice_yaml": to_nice_yaml,
    "verb_to_word": verb_to_word,
    "l0": l0,
    "expand_vars": lambda x: os.path.expandvars(x),
    "dbg": lambda x: __import__("pudb").set_trace(),
}
