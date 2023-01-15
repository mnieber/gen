import os

import yaml

from .add_host_to_type_specs import add_host_to_type_specs
from .resolve_module_names import resolve_module_names
from .type_spec_parser import TypeSpecParser


def load_type_specs(type_reg, spec_dir):
    debug = False
    if debug:
        from pprint import pprint as pp
    else:
        pp = None

    fn = os.path.join(spec_dir, "models.yaml")
    if os.path.exists(fn):
        with open(fn) as f:

            type_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
            parser = TypeSpecParser(type_reg)

            new_dict = parser.parse("server", type_spec_dict["server"])

            if pp:
                pp(new_dict)

            resolve_module_names(type_reg)
            add_host_to_type_specs("client", type_reg)

            new_dict = parser.parse("client", type_spec_dict["client"])
            if pp:
                pp(new_dict)
