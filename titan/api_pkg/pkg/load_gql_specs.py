import os

import yaml
from titan.types_pkg.typeregistry import get_type_reg

from .get_gql_spec import get_gql_spec
from .post_process_gql_specs import post_process_gql_specs


def load_gql_specs(gql_reg, spec_dir):
    fn = os.path.join(spec_dir, "gql.yaml")
    if os.path.exists(fn):
        with open(fn) as f:
            root_gql_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
            get_all_gql_specs(gql_reg, "client", root_gql_spec_dict)
            post_process_gql_specs(gql_reg, get_type_reg())


def get_all_gql_specs(gql_reg, host, root_gql_spec_dict):
    for key, gql_spec_dict in root_gql_spec_dict.items():
        get_gql_spec(gql_reg, host, key, gql_spec_dict)
