import os

import yaml
from moonleap.typespec.load_type_specs.get_field_spec import get_field_spec
from moonleap.typespec.load_type_specs.post_process_type_specs import (
    post_process_type_specs,
)


def load_type_specs(type_spec_store, spec_dir):
    fn = os.path.join(spec_dir, "models.yaml")
    if os.path.exists(fn):
        with open(fn) as f:
            root_type_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
            for first_pass in (True, False):
                get_root_type_spec(type_spec_store, root_type_spec_dict, first_pass)
    post_process_type_specs(type_spec_store)


def get_root_type_spec(type_spec_store, root_type_spec_dict, first_pass):
    root_type_spec_dict["__type_name__"] = "root"
    root_type_spec_dict["__field_names__"] = []
    for key, field_spec_dict in root_type_spec_dict.items():
        if key.startswith("__"):
            continue

        get_field_spec(
            type_spec_store, key, field_spec_dict, root_type_spec_dict, first_pass
        )
