import ramda as R


def css_import_statements(app_module):
    def clean(x):
        x = x.strip()
        if not x.endswith(";"):
            x += ";"
        return x

    css_imports = app_module.css_imports.merged
    for tool in app_module.service.tools:
        css_imports += tool.css_imports.merged

    result = R.pipe(
        R.always(css_imports),
        R.map(R.prop("paths")),
        R.chain(R.identity),
        R.map(clean),
    )(None)

    return result
