from titan.api_pkg.gqlregistry import get_gql_reg


def gql_spec(self):
    return get_gql_reg().get(self.name)
