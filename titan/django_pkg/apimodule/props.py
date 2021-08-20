def _modules(self):
    return [x for x in self.django_app.modules if x.item_types]


class Sections:
    def __init__(self, res):
        self.res = res

    def query_base_classes(self):
        result = "".join(
            [
                f"{x.name_snake}.schema.Query, "
                for x in _modules(self.res)
                if x.has_graphql_queries
            ]
        )
        return (result + "graphene.ObjectType") if result else ""

    def mutation_base_classes(self):
        result = "".join(
            [
                f"{x.name_snake}.schema.Mutation, "
                for x in _modules(self.res)
                if x.has_graphql_mutations
            ]
        )
        return (result + "graphene.ObjectType") if result else ""

    def schema_args(self):
        args = []
        if self.mutation_base_classes():
            args.append("mutation=Mutation")
        if self.query_base_classes():
            args.append("query=Query")
        return ", ".join(args)

    def imports(self):
        return "\n".join(
            [
                f"import {x.name_snake}.schema"
                for x in _modules(self.res)
                if x.has_graphql_mutations or x.has_graphql_queries
            ]
        )
