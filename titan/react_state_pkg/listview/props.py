import ramda as R
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.router.resources import prepend_router_configs
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = get_component_base_url(self, self.item_name)
    result = (
        prepend_router_configs(
            self.load_items_effect.create_router_configs(), [router_config]
        )
        if self.load_items_effect
        else [router_config]
    )

    for state in self.module.states:
        item_names = [x.item_name for x in state.item_lists]
        if state.state_provider and self.item_name in item_names:
            result = prepend_router_configs(
                state.state_provider.create_router_configs(), result
            )

    return result


class Sections:
    def __init__(self, res):
        self.res = res

    def _find_behavior(self, name):
        return R.find(lambda x: x.name == name)(self.res.behaviors)

    def imports(self):
        result = []
        selection_bvr = self._find_behavior("selection")
        if selection_bvr:
            result.append("import { Selection } from 'skandha-mobx/Selection';")
            result.append(
                "import { ClickToSelectItems } from 'skandha-facets/handlers';"
            )

        if self._find_behavior("highlight"):
            result.append("import { Highlight } from 'skandha-mobx/Highlight';")

        return "\n".join(result)

    def default_props(self):
        result = []
        selection_bvr = self._find_behavior("selection")
        if selection_bvr:
            result.extend([f"          {self.res.items_name}Selection: Selection,"])
            result.extend(
                [f"          {self.res.items_name}HandlerClicks: ClickToSelectItems,"]
            )

        if self._find_behavior("highlight"):
            result.extend([f"          {self.res.items_name}Highlight: Highlight,"])

        return "\n".join(result)

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

        return "\n".join(
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
            result.extend([f"{indent}{{...props.{self.res.items_name}HandlerClicks}}"])
        else:
            result.extend(
                [
                    f"{indent}onClick="
                    + f"{{() => alert('TODO: browse to {self.res.item_name}')}}"
                ]
            )

        return "\n".join(result)
