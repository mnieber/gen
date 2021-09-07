import os
from pathlib import Path

from moonleap import render_templates, upper0
from moonleap.resources.type_spec_store import type_spec_store
from titan.django_pkg.apimutation.props import graphene_type_from_field_spec
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


def get_context(item_type, api_module):
    _ = lambda: None
    _.django_app = api_module.django_app
    _.item_name = item_type.name
    _.type_name = upper0(_.item_name)
    _.type_spec = type_spec_store().get(_.type_name)
    _.field_specs = [x for x in _.type_spec.field_specs if x.private]
    _.form_type_name = upper0(_.item_name) + "Form"
    _.form_type_spec = type_spec_store().get(_.form_type_name)
    _.form_field_specs = [x for x in _.form_type_spec.field_specs if not x.private]

    class Sections:
        def imports(self):
            module = find_module_that_provides_item_list(_.django_app, _.item_name)
            return (
                f"from {module.name}.models import {upper0(_.item_name)}"
                if module
                else ""
            )

        def exclude(self):
            list_str = ", ".join([f'"{x.name_snake}"' for x in _.field_specs])
            return f"exclude = [{list_str}]" if list_str else ""

        def form_type_fields(self):
            return os.linesep.join(
                [
                    f'    {x.name_snake} = {graphene_type_from_field_spec(x, "")}'
                    for x in _.form_field_specs
                ]
            )

    return dict(sections=Sections(), _=_)


def render_schema(api_module, item_type, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        item_type,
        write_file,
        render_template,
        output_path=api_module.merged_output_path,
    )
