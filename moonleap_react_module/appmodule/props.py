from moonleap.utils.merge_into_config import merge_into_config
from moonleap_react.component.props import concat_paths


def css_import_lines(app_module):
    css_imports = app_module.css_imports.merged
    for tool in app_module.service.tools:
        css_imports += tool.css_imports.merged

    return concat_paths(css_imports)


def get_flags(app_module):
    result = {}
    for flags in app_module.flags.merged:
        merge_into_config(result, flags.values)

    for tool in app_module.service.tools:
        for flags in tool.flags.merged:
            merge_into_config(result, flags.values)

    return result
