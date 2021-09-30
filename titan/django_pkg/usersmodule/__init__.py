from pathlib import Path

from moonleap import create, kebab_to_camel, kebab_to_snake

from .resources import UsersModule  # noqa


@create("users:module")
def users_module_created(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    module = UsersModule(name_snake=name_snake, name=name)
    module.add_template_dir(Path(__file__).parent / "templates")
    module.output_path = module.name_snake
    module.has_graphql_schema = True
    return module
