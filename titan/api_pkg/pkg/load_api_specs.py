import os

from moonleap import load_yaml
from titan.types_pkg.typeregistry import get_type_reg
from titan.typespec.get_api_spec import get_api_spec


def load_api_specs(api_reg, spec_dir):
    fn = os.path.join(spec_dir, "api.yaml")
    if os.path.exists(fn):
        get_all_api_specs(api_reg, load_yaml(fn))


def get_all_api_specs(api_reg, root_api_spec_dict):
    for key, api_spec_dict in root_api_spec_dict.items():
        api_spec = get_api_spec(
            api_reg, "server", key, api_spec_dict, get_type_reg().type_names
        )
        for output_field_spec in api_spec.outputs_type_spec.field_specs:
            output_field_spec.has_api.append("client")
