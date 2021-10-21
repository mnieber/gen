import os

from moonleap import u0
from titan.react_pkg.pkg.ml_get import ml_react_app


def _panels(view):
    panels = [
        view.left_panel,
        view.right_panel,
        view.top_panel,
        view.bottom_panel,
        view.middle_panel,
    ]
    return [x for x in panels if x]


def _collapses(panel):
    return ml_react_app(panel).service.get_tweak_or(
        True,
        [
            "react_app",
            "components",
            panel.name,
            "collapses",
        ],
    )


def _named_components(panel):
    if _collapses(panel.typ):
        return [x for x in panel.typ.child_components]
    else:
        return [panel]


def _panel(divClassName, panel):
    if not panel:
        return []

    named_components = _named_components(panel)
    if not named_components and not panel.typ.wraps_children:
        return []

    collapses = _collapses(panel.typ)
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
                " " * indent + '<div className="Card">',
                " " * (indent + 2) + f"<h2>{named_component.typ.get_title()}</h2>",
                " " * (indent + 2) + named_component.typ.react_tag,
                " " * indent + "</div>",
            ]
        )

    if collapses:
        indent -= 2
        result.extend(["</div>"])

    return result


def get_context(view):
    _ = lambda: None
    _.view = view
    _.wraps_children = view.wraps_children
    _.panels = _panels(view)
    _.has_col = (
        view.top_panel or view.bottom_panel or not (view.left_panel or view.right_panel)
    )

    class Sections:
        def view_props_type(self):
            result = []
            if _.wraps_children:
                result.append(f"type PropsT = React.PropsWithChildren<{{")
            else:
                result.append(f"type PropsT = {{")

            result.append(r"  className?: any;")

            if _.wraps_children:
                result.append(f"}}>")
            else:
                result.append(f"}}")

            return os.linesep.join(result)

        def view_div(self):
            result = []

            # top section
            if _.has_col:
                rootClass = f"'{view.name}', "
                result.extend(
                    [
                        r"<div",
                        r"  className={classnames(",
                        f"    {rootClass}'flex flex-col w-full', props.className",
                        r"  )}",
                        r">",
                    ]
                )
            result.extend(_panel(view.name + "__topPanel", view.top_panel))

            # mid section
            if view.left_panel or view.right_panel:
                rootClass = (
                    "" if view.top_panel or view.bottom_panel else f"'{view.name}', "
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
            result.extend(_panel(view.name + "__leftPanel", view.left_panel))
            result.extend(_panel(view.name + "__middlePanel", view.middle_panel))
            result.extend(_panel(view.name + "__rightPanel", view.right_panel))

            for named_component in view.child_components:
                if named_component not in _.panels:
                    result.append(f"  {named_component.typ.react_tag}")

            if view.wraps_children and not [
                x for x in view.child_components if x.typ.wraps_children
            ]:
                result.append(r"  {props.children}")

            if view.left_panel or view.right_panel:
                result.append(r"</div>")

            # bottom section
            result.extend(_panel(view.name + "__bottomPanel", view.bottom_panel))
            if _.has_col:
                result.append(r"</div>")

            return "\n".join(result)

        def view_imports(self):
            result = []
            for panel in _.panels:
                for named_component in _named_components(panel):
                    result.append(
                        f"import {{ {u0(named_component.typ.name)} }} from "
                        + f"'{named_component.typ.module.module_path}/components';"
                    )
            return "\n".join(result)

    return dict(sections=Sections())


def skip_render(self):
    return self.parent_view and _collapses(self)
