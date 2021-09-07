import moonleap.resource.props as P
from moonleap import add_src, add_src_inv, extend
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.module import Module

rules = [
    (("django-app", has, "module"), add_src_inv("output_paths")),
    (("django-app", has, "module"), add_src("django_configs")),
]


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(has, "module")


@extend(Module)
class ExtendModule:
    django_app = P.parent(DjangoApp, has)
