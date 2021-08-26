import ramda as R
from moonleap import get_session, render_templates, upper0


def _panels(res):
    panels = [
        res.left_panel,
        res.right_panel,
        res.top_panel,
        res.bottom_panel,
        res.middle_panel,
    ]
    return [x for x in panels if x]


def _collapses(panel):
    return R.path_or(
        True,
        [
            "services",
            panel.module.react_app.service.name,
            "react_app",
            "components",
            panel.name,
            "collapses",
        ],
    )(get_session().get_tweaks())


def _components(panel):
    wraps = panel.wraps_children
    if len(panel.child_components) == 0 and not wraps:
        return None

    collapses = _collapses(panel)
    return panel.child_components if collapses else [panel]


def _panel(divClassName, panel):
    if not panel:
        return []

    collapses = _collapses(panel)
    indent = 2

    if panel.wraps_children and collapses:
        return [" " * indent + "{ props.children }"]

    components = _components(panel)
    if not components:
        return []

    result = []
    if collapses:
        result.extend([f'{" " * indent}<div className="{divClassName}">'])
        indent += 2

    for component in components:
        result.extend([" " * indent + component.react_tag])

    if collapses:
        indent -= 2
        result.extend(["</div>"])

    return result


class Sections:
    def __init__(self, res):
        self.res = res

    def div(self):
        result = []
        has_col = (
            self.res.top_panel
            or self.res.bottom_panel
            or not (self.res.left_panel or self.res.right_panel)
        )

        # top section
        if has_col:
            rootClass = f"'{self.res.name}', "
            result.extend(
                [
                    r"<div",
                    r"  className={classnames(",
                    f"    {rootClass}'flex flex-col w-full', props.className",
                    r"  )}",
                    r">",
                ]
            )
        result.extend(_panel(self.res.name + "__topPanel", self.res.top_panel))

        # mid section
        if self.res.left_panel or self.res.right_panel:
            rootClass = (
                ""
                if self.res.top_panel or self.res.bottom_panel
                else f"'{self.res.name}', "
            )
            result.extend(
                [
                    r"<div",
                    r"  className={classnames(",
                    f"    {rootClass}'flex flex-row', props.className",
                    r"  )}",
                    r">",
                ]
            )
        result.extend(_panel(self.res.name + "__leftPanel", self.res.left_panel))
        result.extend(_panel(self.res.name + "__middlePanel", self.res.middle_panel))
        result.extend(_panel(self.res.name + "__rightPanel", self.res.right_panel))

        panels = _panels(self.res)
        result.extend(
            [f"  {x.react_tag}" for x in self.res.child_components if x not in panels]
        )

        if self.res.left_panel or self.res.right_panel:
            result.append(r"</div>")

        # bottom section
        result.extend(_panel(self.res.name + "__bottomPanel", self.res.bottom_panel))
        if has_col:
            result.append(r"</div>")

        return "\n".join(result)

    def imports(self):
        result = []
        for panel in _panels(self.res):
            for component in _components(panel):
                result.append(
                    f"import {{ {upper0(component.name)} }} from '{component.module_path}/components';"  # noqa: E501
                )
        return "\n".join(result)


def render(self, write_file, render_template):
    if self.parent_view and _collapses(self):
        return

    return render_templates(self.root_filename, self.templates_dir)(
        self, write_file, render_template
    )
