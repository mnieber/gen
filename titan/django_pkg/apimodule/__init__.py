from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, extend
from moonleap.utils.case import kebab_to_camel, sn
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp

from . import props
from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term, block):
    module = ApiModule(name=kebab_to_camel(term.data))
    module.output_path = sn(module.name)
    module.add_template_dir(Path(__file__).parent / "templates")
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")


@extend(ApiModule)
class ExtendApiModule:
    render = MemFun(props.render)
    graphql_api = P.child(has, "graphql:api")
