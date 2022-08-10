from pathlib import Path

from moonleap import create, kebab_to_camel
from moonleap.utils.case import sn

from .get_context import get_context
from .resources import UsersModule  # noqa


@create("users:module")
def users_module_created(term):
    name = kebab_to_camel(term.data)
    module = UsersModule(name=name)
    module.add_template_dir(Path(__file__).parent / "templates", get_context)
    module.output_path = sn(module.name)
    module.has_graphql_schema = True
    return module
