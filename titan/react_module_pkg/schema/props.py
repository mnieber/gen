import os
from pathlib import Path

from moonleap import render_templates
from moonleap.utils.case import l0
from titan.react_module_pkg.apiquery.props import define_schema_field


def get_context(item_types, api_module):
    _ = lambda: None
    _.api_module = api_module
    _.item_types = item_types

    class Sections:
        def schema_fields(self, item_type):
            result = []
            fk_field_specs = item_type.type_spec.get_field_specs(["fk", "relatedSet"])
            for field_spec in fk_field_specs:
                result.append(define_schema_field(field_spec, l0(item_type.name)))
            return os.linesep.join(result)

    return dict(sections=Sections(), _=_)


def render_schema(api_module, item_types, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        sorted(item_types, key=lambda x: x.name),
        write_file,
        render_template,
        output_path=api_module.merged_output_path,
    )
