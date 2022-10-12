import os

import yaml

from .add_host_to_type_specs import add_host_to_type_specs
from .type_spec_parser import TypeSpecParser


def load_type_specs(type_spec_store, spec_dir):
    fn = os.path.join(spec_dir, "models.yaml")
    if os.path.exists(fn):
        with open(fn) as f:
            type_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
            __import__("pudb").set_trace()
            parser = TypeSpecParser(type_spec_store)
            new_dict = parser.parse("server", type_spec_dict["server"])

            from pprint import pprint as pp

            pp(new_dict)

            add_host_to_type_specs("client", type_spec_store)
            parser.parse("client", type_spec_dict["client"])
