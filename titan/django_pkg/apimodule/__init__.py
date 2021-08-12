import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, kebab_to_snake, tags
from moonleap.utils.case import snake_to_camel
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp

from . import props
from .resources import ApiModule  # noqa


@tags(["api:module"])
def create_api_module(term, block):
    name_snake = kebab_to_snake(term.data)
    module = ApiModule(name_snake=name_snake, name=snake_to_camel(name_snake))
    module.output_path = module.name_snake
    module.add_template_dir(__file__, "templates")
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")


@extend(ApiModule)
class ExtendApiModule:
    p_section_base_classes = MemFun(props.p_section_base_classes)
    p_section_imports = Prop(props.p_section_imports)
