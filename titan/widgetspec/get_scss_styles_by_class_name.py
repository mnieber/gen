def get_scss_styles_by_class_name(widget_spec):
    result = {}
    queue = [widget_spec]
    while queue:
        widget_spec = queue.pop()
        styles = _get_scss_styles(widget_spec)
        if styles:
            result[widget_spec.widget_class_name] = styles
        queue += widget_spec.child_widget_specs
    return result


def _get_scss_styles(widget_spec):
    result = []
    for style in widget_spec.div.styles:
        if False:
            result.append(style)
    return result
