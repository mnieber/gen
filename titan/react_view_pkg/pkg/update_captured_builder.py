from moonleap.utils.case import kebab_to_camel, l0
from moonleap.utils.inflect import plural


def update_captured_builder(builder):
    b = builder
    captured_array = None
    captured_field = None
    while not (captured_array or captured_field) and b:
        captured_array = b if b.widget_spec.values.get("array", False) else None
        captured_field = b if b.widget_spec.values.get("capture", False) else None
        b = b.parent_builder

    const_name = l0(
        kebab_to_camel(
            (
                builder.widget_spec.widget_type or builder.widget_spec.widget_base_type
            ).replace(":", "-")
        )
    )
    if captured_array:
        const_name = plural(const_name)

    prefix, suffix = None, None
    if captured_array and builder is captured_array:
        prefix = f"const {const_name} = R.map(x => ("
        suffix = "), ['Moonleap Todo']);"
    elif captured_field and builder is captured_field:
        prefix = f"const {const_name} = ("
        suffix = ");"

    captured_builder = captured_array or captured_field
    if captured_builder and captured_builder is builder:
        id = captured_builder.widget_spec.id
        preamble_lines = builder.output.preamble_lines_by_id.setdefault(id, [])
        postamble_lines = builder.output.postamble_lines_by_id.setdefault(id, [])

        if prefix:
            preamble_lines.append(prefix)
            builder.output.lines.append(f"{{{const_name}}}")
        if suffix:
            postamble_lines.append(suffix)

    return captured_builder
