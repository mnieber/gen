from moonleap.gqlspec.gql_spec_store import gql_spec_store


def gql_spec(self):
    return gql_spec_store().get(self.name)
