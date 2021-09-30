import os
from pathlib import Path

from moonleap import render_templates
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name
from titan.react_module_pkg.apiquery.props import define_schema_field


def get_context(item_type, api_module):
    _ = lambda: None
    _.api_module = api_module
    _.item_type = item_type
    _.item_name = _.item_type.name
    _.schema_name = _.item_name
    _.type_spec = ml_type_spec_from_item_name(_.item_name)
    _.fk_field_specs = [
        x for x in _.type_spec.field_specs if x.field_type in ("fk", "related_set")
    ]

    class Sections:
        def schema_imports(self):
            result = []
            for field_spec in _.fk_field_specs:
                fk_item_name = field_spec.field_type_attrs["target"]
                result.append(
                    f"import {{ {fk_item_name} }} from 'src/api/schemas/{fk_item_name}Schema';"
                )

            return os.linesep.join(result)

        def schema_fields(self):
            result = []
            for field_spec in _.fk_field_specs:
                result.append(define_schema_field(field_spec, _.schema_name))
            return os.linesep.join(result)

    return dict(sections=Sections(), _=_)


def render_schema(api_module, item_type, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        item_type,
        write_file,
        render_template,
        output_path=api_module.merged_output_path,
    )
