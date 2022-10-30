import os

from moonleap import u0


def _panels(view):
    panels = [
        view.left_panel,
        view.right_panel,
        view.top_panel,
        view.bottom_panel,
        view.middle_panel,
    ]
    return [x for x in panels if x]


def _named_components(panel):
    if panel.typ.collapses:
        return list(panel.typ.child_components)
    else:
        return [panel]


def _panel(divClassName, panel):
    if not panel:
        return []

    named_components = _named_components(panel)
    if not named_components and not panel.typ.wraps_children:
        return []

    collapses = panel.typ.collapses
    indent = 2
    result = []

    if collapses:
        result.extend([f'{" " * indent}<div className="{divClassName}">'])
        indent += 2
        if panel.typ.wraps_children:
            result.extend([" " * indent + r"{props.children}"])

    for named_component in named_components:
        result.extend(
            [
                " " * indent + named_component.typ.react_tag,
            ]
        )

    if collapses:
        indent -= 2
        result.extend(["</div>"])

    return result


def get_helpers(_):
    class Helpers:
        view = _.component
        panels = _panels(view)
        wraps_children = view.wraps_children or [
            x for x in panels if x.typ.wraps_children and x.typ.collapses
        ]
        has_col = (
            view.top_panel
            or view.bottom_panel
            or not (view.left_panel or view.right_panel)
        )

        def view_props_type(self):
            result = []
            if self.wraps_children:
                result.append(f"type PropsT = React.PropsWithChildren<{{")
            else:
                result.append(f"type PropsT = {{")

            result.append(r"  className?: any;")

            if self.wraps_children:
                result.append(f"}}>")
            else:
                result.append(f"}}")

            return os.linesep.join(result)

        def view_div(self):
            result = []

            # top section
            if self.has_col:
                rootClass = f"'{self.view.name}', "
                result.extend(
                    [
                        r"<div",
                        r"  className={cn(",
                        f"    {rootClass}'flex flex-col w-full', props.className",
                        r"  )}",
                        r">",
                    ]
                )
            result.extend(_panel(self.view.name + "__TopPanel", self.view.top_panel))

            # mid section
            if self.view.left_panel or self.view.right_panel:
                rootClass = (
                    ""
                    if self.view.top_panel or self.view.bottom_panel
                    else f"'{self.view.name}', "
                )
                result.extend(
                    [
                        r"<div",
                        r"  className={cn(",
                        f"    {rootClass}'flex flex-row', props.className",
                        r"  )}",
                        r">",
                    ]
                )
            result.extend(_panel(self.view.name + "__LeftPanel", self.view.left_panel))
            result.extend(
                _panel(self.view.name + "__MiddlePanel", self.view.middle_panel)
            )
            result.extend(
                _panel(self.view.name + "__RightPanel", self.view.right_panel)
            )

            for named_component in self.view.child_components:
                if named_component not in self.panels:
                    result.append(f"  {named_component.typ.react_tag}")

            if self.view.wraps_children and not [
                x for x in self.panels if x.typ.wraps_children
            ]:
                result.append(r"  {props.children}")

            if self.view.left_panel or self.view.right_panel:
                result.append(r"</div>")

            # bottom section
            result.extend(
                _panel(self.view.name + "__BottomPanel", self.view.bottom_panel)
            )
            if self.has_col:
                result.append(r"</div>")

            return "\n".join(result)

        def view_imports(self):
            result = []
            for panel in [self.view, *self.panels]:
                named_components = (
                    list(panel.child_components)
                    if panel is self.view
                    else _named_components(panel)
                )
                for named_component in named_components:
                    result.append(
                        f"import {{ {u0(named_component.typ.name)} }} from "
                        + f"'src/{named_component.typ.module.module_path}/components';"
                    )
            return "\n".join(result)

    return Helpers()
