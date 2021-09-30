import moonleap.resource.props as P
from moonleap import extend, feeds, receives
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.module import Module

rules = [
    (("django-app", has, "module"), feeds("output_paths")),
    (("django-app", has, "module"), receives("django_configs")),
]


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(has, "module")


@extend(Module)
class ExtendModule:
    django_app = P.parent("django-app", has, required=True)
