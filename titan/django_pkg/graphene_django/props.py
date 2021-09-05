from moonleap.render.template_renderer import render_templates
from moonleap.resources.data_type_spec_store import FK, data_type_spec_store

from .endpoint_sections import EndPointSectionsMixin
from .type_sections import TypeSectionsMixin


def render(self, write_file, render_template):
    for module in self.service.django_app.modules:
        if module.item_types or module.forms:
            render_templates(__file__, "templates_module", graphene=self)(
                module, write_file, render_template
            )


def has_graphql_mutations(module):
    return bool(module.forms or module.items_received)


def has_graphql_queries(module):
    return bool(module.item_lists_provided)


class Sections(EndPointSectionsMixin, TypeSectionsMixin):
    def __init__(self, res):
        self.res = res
