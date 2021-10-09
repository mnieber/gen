import os
from pathlib import Path

from moonleap import render_templates, u0
from moonleap.utils.case import sn
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


def get_context(item_type, api_module):
    _ = lambda: None
    _.django_app = api_module.django_app
    _.item_name = item_type.name
    _.type_spec = ml_type_spec_from_item_name(_.item_name)
    _.fk_field_specs = _.type_spec.get_field_specs(["fk"])
    _.private_field_specs = [x for x in _.type_spec.field_specs if x.private]
    _.form_type_spec = ml_form_type_spec_from_item_name(_.item_name)
    _.form_field_specs = [x for x in _.form_type_spec.field_specs if not x.private]

    class Sections:
        def graphql_type_imports(self):
            module = find_module_that_provides_item_list(_.django_app, _.item_name)
            return (
                f"from {module.name}.models import {u0(_.item_name)}" if module else ""
            )

        def graphql_type_fields(self):
            list_str = ", ".join([f'"{sn(x.name)}"' for x in _.private_field_specs])
            return f"exclude = [{list_str}]" if list_str else ""

        def graphql_type_exclude(self):
            list_str = ", ".join([f'"{sn(x.name)}"' for x in _.private_field_specs])
            return f"exclude = [{list_str}]" if list_str else ""

        def form_type_fields(self):
            return os.linesep.join(
                [
                    f'    {sn(x.name)} = {x.graphene_output_type("")}'
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
