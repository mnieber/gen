import pytest
from graphene_django.utils.testing import graphql_query


class GraphqlTestCase:
    @pytest.fixture()
    def client_query(self, client):
        def func(*args, **kwargs):
            return graphql_query(*args, **kwargs, client=client)

        return func
