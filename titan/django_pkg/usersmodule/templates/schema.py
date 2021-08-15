import django_rtk_green.mutations
import django_rtk_green.queries
import graphene
import graphql_jwt


class Mutation(django_rtk_green.mutations.Mutation, graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(django_rtk_green.queries.Query, graphene.ObjectType):
    pass
