from moonleap.utils.case import kebab_to_camel, l0
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.create_widget_class_name import create_widget_class_name


def get_root_builder(builder):
    b = builder.parent_builder
    while b:
        if b.is_captured or not b.parent_builder:
            return b
        b = b.parent_builder
    return None


def create_preamble(builder, output):
    output.preamble_lines = []
    output.postamble_lines = []
    if builder.is_captured:
        const_name = l0(
            kebab_to_camel(
                (
                    builder.widget_spec.widget_name
                    or builder.widget_spec.widget_base_type
                ).replace(":", "-")
            )
        )

        prefix, suffix = None, None
        if builder.is_captured == "array":
            prefix = f"const {const_name} = " + "['Moonleap Todo'].map(x => { return ("
            suffix = "); });"
        else:
            prefix = f"const {const_name} = ("
            suffix = ");"

        output.preamble_lines.append(prefix)
        output.lines.append(f"{{{const_name}}}")
        output.postamble_lines.append(suffix)


def create_builder_output(builder):
    output = BuilderOutput(widget_class_name=create_widget_class_name(builder))
    _register_components(builder, output)
    create_preamble(builder, output)
    return output


def _register_components(builder, output):
    if builder.widget_spec.is_component and builder.level > 0:
        output.components.append(builder.widget_spec.component)
