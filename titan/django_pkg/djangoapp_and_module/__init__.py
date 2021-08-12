import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.module import Module


@rule("django-app", has, "module")
def django_app_has_module(django_app, module):
    module.output_paths.add_source(django_app)
    django_app.django_configs.add_source(module)


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(has, "module")


@extend(Module)
class ExtendModule:
    django_app = P.parent(DjangoApp, has)
