from moonleap import create
from titan.project_pkg.service import Tool

base_tags = [
    ("graphql-auth", ["tool"]),
]


@create("graphql-auth")
def create_graphql_auth(term):
    return Tool(name="graphql_auth")
