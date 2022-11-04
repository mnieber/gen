import os

from moonleap import load_yaml

from .get_gql_spec import get_gql_spec


def load_gql_specs(gql_reg, spec_dir):
    fn = os.path.join(spec_dir, "gql.yaml")
    if os.path.exists(fn):
        get_all_gql_specs(gql_reg, "client", load_yaml(fn))


def get_all_gql_specs(gql_reg, host, root_gql_spec_dict):
    for key, gql_spec_dict in root_gql_spec_dict.items():
        get_gql_spec(gql_reg, host, key, gql_spec_dict)
