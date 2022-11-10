from moonleap import create, create_forward, empty_rule, rule
from moonleap.session import get_session
from moonleap.verbs import has
from titan.widgets_pkg.pkg.load_widget_specs import load_widget_specs

from .resources import WidgetRegistry

rules = {
    ("project", has, "widget-registry"): empty_rule(),
}

_widget_registry = None


def get_widget_reg():
    global _widget_registry
    if not _widget_registry:
        _widget_registry = WidgetRegistry()
        load_widget_specs(_widget_registry, get_session().spec_dir)

    return _widget_registry


@create("widget-registry")
def create_widget_registry(term):
    global _widget_registry
    if _widget_registry:
        raise Exception("The widget registry should be created only once")

    return get_widget_reg()


@rule("project")
def created_project(project):
    return create_forward(project, has, ":widget-registry")


@rule("widget-registry")
def created_widget_registry(widget_registry):
    # lut = get_map_from_widget_to_react_module(react_app.modules)
    pass
