import ramda as R
from moonleap import get_tweaks, upper0
from moonleap_react.component.resources import get_component_base_url
from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router.resources import reduce_router_configs


def _get_route_params(self):
    return R.path_or(
        [],
        ["services", self.module.service.name, "components", self.name, "route_params"],
    )(get_tweaks())


def _wraps(panel):
    return panel and panel.shows_children


def create_router_configs(self):
    base_url = get_component_base_url(self, "")
    url = "/".join(
        ([base_url] if base_url else [])
        + [":" + x for x in _get_route_params(self) if x is not None]
    )
    router_config = RouterConfig(
        component=self,
        url=url,
        wraps=_wraps(self.top_panel)
        or _wraps(self.middle_panel)
        or _wraps(self.bottom_panel)
        or _wraps(self.left_panel)
        or _wraps(self.right_panel),
    )
    result = reduce_router_configs([router_config])
    return result


def _panel(divClassName, panel):
    if not panel:
        return []

    if panel.shows_children:
        return ["{ props.children }"]

    component = panel.root_component
    if not component:
        return []

    result = []
    collapses = panel.collapses
    indent = 2
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

    # top section
    if self.top_panel or self.bottom_panel:
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
    if self.left_panel or self.right_panel:
        result.append(r"</div>")

    # bottom section
    result.extend(_panel(self.name + "__bottomPanel", self.bottom_panel))
    if self.top_panel or self.bottom_panel:
        result.append(r"</div>")

    return "\n".join(result)


def p_section_imports(self):
    result = []
    for panel in [
        self.left_panel,
        self.right_panel,
        self.top_panel,
        self.bottom_panel,
        self.middle_panel,
    ]:
        if panel:
            component = panel.root_component
            if component:
                result.append(
                    f"import {{ {upper0(component.name)} }} from '{component.module_path}/components';"
                )
    return "\n".join(result)
