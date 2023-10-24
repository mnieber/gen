from moonleap import append_uniq, u0
from moonleap.utils.indent import indent


def get_helpers(_):
    class Helpers:
        view = _.component
        main_div = ""
        imported_components = []

        def __init__(self):
            self.level = 6
            self.render_main_div()

        def render_main_div(self):
            self.imported_components = []
            self.main_div = ""

            name = self.view.name
            classnames_str = f'"{name}", [props.className]'

            result = indent(self.level)(
                tpl_main_open.format(name=name, classnames=classnames_str)
            )

            self.level += 2
            for named_component in self.view.named_components:
                append_uniq(self.imported_components, named_component.typ)
                result += indent(self.level)(
                    tpl_component.format(name=named_component.typ.name)
                )

            for named_div in self.view.named_divs:
                result += self.render_named_div(named_div)
            self.level -= 2

            result += indent(self.level)(tpl_close)
            self.main_div = result

        def render_named_div(self, named_div):
            name = named_div.typ.name
            classnames_str = ",".join(named_div.typ.classnames)

            result = indent(self.level)(
                tpl_open.format(name=name, classnames=classnames_str)
            )

            self.level += 2
            for named_component in named_div.named_components:
                append_uniq(self.imported_components, named_component.typ)
                result += indent(self.level)(
                    tpl_component.format(name=named_component.typ.name)
                )

            for named_div in named_div.named_divs:
                result += self.render_named_div(named_div)
            self.level -= 2

            result += indent(self.level)(tpl_close)
            return result

    return Helpers()


tpl_main_open = """/*
🔳 {name} 🔳
*/
<div className={{cn({classnames})}}>
"""


tpl_open = """{{
// 🔳 {name} 🔳
}}
<div className={{cn({classnames})}}>
"""


tpl_close = """</div>
"""

tpl_component = """<{name} />
"""


def get_meta_data_by_fn(_, __):
    return {
        "View.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
        "View.scss.j2": {
            "name": f"{u0(_.component.name)}.scss",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "view"
    ]
