from moonleap.utils.case import l0
from moonleap.utils.inflect import plural


def get_capture_elements(builder):
    b = builder
    captured_array = None
    captured_field = None
    while not (captured_array or captured_field) and b:
        captured_array = b if b.widget_spec.values.get("array", False) else None
        captured_field = b if b.widget_spec.values.get("capture", False) else None
        b = b.parent_builder

    const_name = l0(
        builder.widget_spec.widget_type or builder.widget_spec.widget_base_type
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
    return captured_array or captured_field, const_name, prefix, suffix
