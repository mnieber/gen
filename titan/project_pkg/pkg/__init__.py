import io
import json
import os

import jinja2
from moonleap.spec.term import verb_to_word
from moonleap.utils import chop_suffix, dbg
from moonleap.utils.case import camel_to_kebab, l0, sn, u0
from moonleap.utils.inflect import plural
from moonleap.utils.ruamel_yaml import ruamel_yaml


def sort_dict(item: dict):
    return {
        k: sort_dict(v) if isinstance(v, dict) else v for k, v in sorted(item.items())
    }


def to_nice_json(value):
    return json.dumps(value, sort_keys=False, indent=2, separators=(",", ": "))


def to_nice_yaml(value):
    with io.StringIO() as f:
        ruamel_yaml.dump(sort_dict(value), stream=f)
        return f.getvalue()


def dot(x, path):
    result = x
    for part in path.split("."):
        if result is None or isinstance(result, jinja2.runtime.Undefined):
            return result
        result = (
            result.get(part)
            if isinstance(result, dict)
            else getattr(result, part, None)
        )
    return result


filters = {
    "bool": lambda x: bool(x),
    "dbg": dbg,
    "dot": dot,
    "chop_suffix": chop_suffix,
    "expand_vars": lambda x: os.path.expandvars(x),
    "l0": l0,
    "negate": lambda x: not bool(x),
    "plural": lambda x: plural(x),
    "sn": sn,
    "to_nice_json": to_nice_json,
    "to_nice_yaml": to_nice_yaml,
    "to_str": lambda x: x if x is None else str(x),
    "u0": u0,
    "verb_to_word": verb_to_word,
    "camel_to_kebab": camel_to_kebab,
}
