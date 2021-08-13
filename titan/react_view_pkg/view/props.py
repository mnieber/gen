import ramda as R
from moonleap import get_session, render_templates, upper0


def _panels(self):
    panels = [
        self.left_panel,
        self.right_panel,
        self.top_panel,
        self.bottom_panel,
        self.middle_panel,
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


def _root_component(panel):
    wraps = panel.wraps_children
    if len(panel.child_components) == 0 and not wraps:
        return None

    collapses = _collapses(panel)
    return (
        panel.child_components[0]
        if len(panel.child_components) == 1 and collapses
        else panel
    )


def _panel(divClassName, panel):
    if not panel:
        return []

    collapses = _collapses(panel)
    indent = 2

    if panel.wraps_children and collapses:
        return [" " * indent + "{ props.children }"]

    component = _root_component(panel)
    if not component:
        return []

    result = []
    if collapses:
        result.extend([f'{" " * indent}<div className="{divClassName}">'])
        indent += 2

    result.extend([" " * indent + component.react_tag])

    if collapses:
        indent -= 2
        result.extend(["</div>"])

    return result


def p_section_div(self):
    result = []
    has_col = (
        self.top_panel or self.bottom_panel or not (self.left_panel or self.right_panel)
    )

    # top section
    if has_col:
        rootClass = f"'{self.name}', "
        result.extend(
            [
                r"<div",
                r"  className={classnames(",
                f"    {rootClass}'flex flex-col', props.className",
                r"  )}",
                r">",
            ]
        )
    result.extend(_panel(self.name + "__topPanel", self.top_panel))

    # mid section
    if self.left_panel or self.right_panel:
        rootClass = "" if self.top_panel or self.bottom_panel else f"'{self.name}', "
        result.extend(
            [
                r"<div",
                r"  className={classnames(",
                f"    {rootClass}'flex flex-row', props.className",
                r"  )}",
                r">",
            ]
        )
    result.extend(_panel(self.name + "__leftPanel", self.left_panel))
    result.extend(_panel(self.name + "__middlePanel", self.middle_panel))
    result.extend(_panel(self.name + "__rightPanel", self.right_panel))

    panels = _panels(self)
    result.extend(
        [f"  {x.react_tag}" for x in self.child_components if x not in panels]
    )

    if self.left_panel or self.right_panel:
        result.append(r"</div>")

    # bottom section
    result.extend(_panel(self.name + "__bottomPanel", self.bottom_panel))
    if has_col:
        result.append(r"</div>")

    return "\n".join(result)


def p_section_imports(self):
    result = []
    for panel in _panels(self):
        component = _root_component(panel)
        if component:
            result.append(
                f"import {{ {upper0(component.name)} }} from '{component.module_path}/components';"  # noqa
            )
    return "\n".join(result)


def render(self, output_root_dir, template_renderer):
    if self.parent_view and len(self.child_components) == 1 and _collapses(self):
        return []

    return render_templates(self.root_filename, self.templates_dir)(
        self, output_root_dir, template_renderer
    )
