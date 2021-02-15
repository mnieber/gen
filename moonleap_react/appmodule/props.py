from moonleap_react.component.props import concat_paths


def css_import_lines(app_module):
    css_imports = app_module.css_imports.merged
    for tool in app_module.service.tools:
        css_imports += tool.css_imports.merged

    return concat_paths(css_imports)
