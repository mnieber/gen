import os

import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store


class Sections:
    def __init__(self, res):
        self.res = res

    def _find_behavior(self, name):
        return R.find(lambda x: x.name == name)(self.res.behaviors)

    def imports(self):
        result = []
        selection_bvr = self._find_behavior("selection")
        if selection_bvr:
            result.append("import { Selection } from 'skandha-facets/Selection';")
            result.append(
                "import { ClickToSelectItems } from 'skandha-facets/handlers';"
            )

        if self._find_behavior("highlight"):
            result.append("import { Highlight } from 'skandha-facets/Highlight';")

        return os.linesep.join(result)

    def default_props(self):
        result = []
        selection_bvr = self._find_behavior("selection")
        if selection_bvr:
            result.extend([f"          {self.res.items_name}Selection: Selection,"])

        if self._find_behavior("highlight"):
            result.extend([f"          {self.res.items_name}Highlight: Highlight,"])

        return os.linesep.join(result)

    def classnames(self):
        result = []
        if self._find_behavior("selection"):
            result.extend(
                [
                    f"          '{self.res.name}Item--selected':",
                    f"            x && props.{self.res.items_name}Selection.ids.includes(x.id),",  # noqa: E501
                ]
            )

        if self._find_behavior("highlight"):
            result.extend(
                [
                    f"          '{self.res.name}Item--highlighted':",
                    f"            x && props.{self.res.items_name}Highlight.id == x.id,",  # noqa: E501
                ]
            )

        if not result:
            return ""

        return os.linesep.join(
            [
                #
                "        className={classnames({",
                *result,
                "        })}",
            ]
        )

    def on_click(self):
        result = []
        indent = " " * 10
        if self._find_behavior("selection"):
            result.extend([f"{indent}{{...handlerClick.handle(x.id)}}"])
        else:
            result.extend(
                [
                    f"{indent}onClick="
                    + f"{{() => alert('TODO: browse to {self.res.item_name}')}}"
                ]
            )

        return os.linesep.join(result)

    def body(self):
        result = []
        selection_bvr = self._find_behavior("selection")
        if selection_bvr:
            result.append(r"const handlerClick = new ClickToSelectItems({")
            result.append(f"  selection: props.{self.res.items_name}Selection")
            result.append(r"});")

        return os.linesep.join(result)

    def fields(self):
        result = []

        type_spec = type_spec_store().get(upper0(self.res.item_name))
        for field_spec in type_spec.field_specs:
            if (
                field_spec.private
                or field_spec.name in ("id",)
                or field_spec.field_type in ("slug",)
            ):
                continue
            result.append(
                f"<div>{field_spec.name}: {{props.{self.res.item_name}.{field_spec.name} }}</div>"
            )
        return os.linesep.join(" " * 6 + line for line in result)


def get_context(self):
    return dict(sections=Sections(self))
