from moonleap.parser.term import word_to_term
from moonleap.utils.case import l0
from moonleap.utils.inflect import plural
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
        is_array = builder.is_captured == "array"
        name = l0(
            builder.widget_spec.widget_name or builder.widget_spec.widget_base_type
        )
        term = word_to_term(name)
        const_name = term.to_camel() if term else name
        if is_array:
            const_name = plural(const_name)

        prefix, suffix = None, None
        if is_array:
            prefix = [f"const {const_name} = " + "['Moonleap Todo'].map(x => {"]
            suffix = ["});"]
        else:
            prefix = [f"const {const_name} = " + "(x => {"]
            suffix = ["})('Moonleap Todo');"]

        output.preamble_lines.extend(prefix)
        output.const_name = const_name
        output.postamble_lines.extend(suffix)


def create_builder_output(builder):
    output = BuilderOutput(
        widget_class_name=create_widget_class_name(builder),
        is_captured=builder.is_captured,
    )
    _register_components(builder, output)
    create_preamble(builder, output)
    return output


def _register_components(builder, output):
    if builder.widget_spec.is_component and builder.level > 0:
        output.components.append(builder.widget_spec.component)
