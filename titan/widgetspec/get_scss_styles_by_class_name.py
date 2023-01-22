from titan.widgetspec.styles import get_style_groups


def get_scss_styles_by_class_name(widget_spec):
    result = {}
    imports = []
    queue = [widget_spec]
    while queue:
        widget_spec = queue.pop()
        more_imports, styles = _get_scss_styles(widget_spec)
        if styles:
            result[widget_spec.widget_class_name] = styles
            imports += more_imports
        queue += widget_spec.child_widget_specs
    return imports, result


def _get_scss_styles(widget_spec):
    imports = []
    styles = []
    for style in widget_spec.div.styles:
        for group in get_style_groups():
            apply = []
            rules = []

            for pattern in group:
                if pattern.is_scss and pattern.match(style):
                    if pattern.is_tailwind:
                        apply.append(style)
                    else:
                        rules.append(f"@include {style}();")
                    imports += pattern.scss_imports

            if apply:
                styles.append("@apply " + " ".join(apply) + ";")

            if rules:
                styles.extend(rules)

    return imports, styles
