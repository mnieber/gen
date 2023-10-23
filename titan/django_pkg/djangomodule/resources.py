from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DjangoModule(Resource):
    name: str
    kebab_name: str
    # Note that most the graphql api is directly defined in the api module
    # (we're not using a separate schema per module).
    # However, there may be other modules that have a graphql schema.
    # These models have the has_graphql_schema set to true.
    has_graphql_schema: bool = False
