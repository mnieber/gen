from pathlib import Path

from moonleap import render_templates


def _fields(type_spec):
    return [
        field_spec for field_spec in type_spec.field_specs if not field_spec.private
    ]


def get_context(item_type, api_module):
    __import__("pudb").set_trace()
    _ = lambda: None
    _.api_module = api_module
    _.item_type = item_type

    class Sections:
        def define_fields(self):
            result = []
            tab = " " * 2

            type_spec = type_spec_store().get(upper0(item_name))
            for field_spec in _fields(type_spec):
                if field_spec.field_type in ("related_set",):
                    fk_item_name = field_spec.field_type_attrs["item_name"]
                    result.append(
                        f"{item_name}.define({{ {field_spec.name}: [{fk_item_name}] }});"
                    )

                if field_spec.field_type in ("fk",):
                    fk_item_name = field_spec.field_type_attrs["item_name"]
                    result.append(
                        f"{item_name}.define({{ {field_spec.name}: {fk_item_name} }});"
                    )

            return ("," + os.linesep).join(result)

    return dict(sections=Sections(), _=_)


def render_schema(api_module, item_type, write_file, render_template):
    __import__("pudb").set_trace()
    template_path = Path(__file__).parent / "templates"
    render_templates(
        template_path,
        get_context=get_context,
        api_module=api_module,
    )(item_type, write_file, render_template, output_path=api_module.merged_output_path)
