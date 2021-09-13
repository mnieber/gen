from pathlib import Path

from moonleap.render.template_renderer import render_templates

from .endpoint_sections import EndPointSectionsMixin
from .type_sections import TypeSectionsMixin


def render(self, write_file, render_template):
    for module in self.service.django_app.modules:
        if module.item_types or module.forms:
            template_path = Path(__file__).parent / "templates_module"
            render_templates(template_path, graphene=self)(
                module, write_file, render_template
            )


def has_graphql_mutations(module):
    return bool(module.forms or module.items_received)


def has_graphql_queries(module):
    return bool(module.item_lists_provided)


class Sections(EndPointSectionsMixin, TypeSectionsMixin):
    def __init__(self, res):
        self.res = res
