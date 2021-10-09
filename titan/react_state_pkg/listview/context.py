import os

import ramda as R
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def get_context(list_view):
    _ = lambda: None
    _.type_spec = ml_type_spec_from_item_name(list_view.item_name)

    class Sections:
        def _find_behavior(self, name):
            return R.find(lambda x: x.name == name)(list_view.behaviors)

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
                result.extend(
                    [f"          {list_view.items_name}Selection: Selection,"]
                )

            if self._find_behavior("highlight"):
                result.extend(
                    [f"          {list_view.items_name}Highlight: Highlight,"]
                )

            return os.linesep.join(result)

        def classnames(self):
            result = []
            if self._find_behavior("selection"):
                result.extend(
                    [
                        f"          '{list_view.name}Item--selected':",
                        f"            x && props.{list_view.items_name}Selection.ids.includes(x.id),",  # noqa: E501
                    ]
                )

            if self._find_behavior("highlight"):
                result.extend(
                    [
                        f"          '{list_view.name}Item--highlighted':",
                        f"            x && props.{list_view.items_name}Highlight.id == x.id,",  # noqa: E501
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
                        + f"{{() => alert('TODO: browse to {list_view.item_name}')}}"
                    ]
                )

            return os.linesep.join(result)

        def body(self):
            result = []
            selection_bvr = self._find_behavior("selection")
            if selection_bvr:
                result.append(r"const handlerClick = new ClickToSelectItems({")
                result.append(f"  selection: props.{list_view.items_name}Selection")
                result.append(r"});")

            return os.linesep.join(result)

        def fields(self):
            result = []

            for field_spec in _.type_spec.field_specs:
                if (
                    field_spec.private
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    continue

                if field_spec.field_type in ("boolean"):
                    value = (
                        f"props.{list_view.item_name}.{field_spec.name} ? 'Yes' : 'No'"
                    )
                else:
                    value = f"props.{list_view.item_name}.{field_spec.name}"

                result.append(f"<div>{field_spec.name}: {{{value}}}</div>")
            return os.linesep.join(" " * 6 + line for line in result)

    return dict(sections=Sections(), _=_)
