from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, extend, kebab_to_snake
from moonleap.utils.case import snake_to_camel
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp

from . import props
from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term, block):
    name_snake = kebab_to_snake(term.data)
    module = ApiModule(name_snake=name_snake, name=snake_to_camel(name_snake))
    module.output_path = module.name_snake
    module.add_template_dir(Path(__file__).parent / "templates")
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")


@extend(ApiModule)
class ExtendApiModule:
    render = MemFun(props.render)
    graphql_api = P.child(has, "graphql:api")
