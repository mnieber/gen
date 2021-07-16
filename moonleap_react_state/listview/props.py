import ramda as R
from moonleap_react.component.resources import get_component_base_url
from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = get_component_base_url(self, self.item_name)
    result = prepend_router_configs(
        self.load_items_effect.create_router_configs(), [router_config]
    )

    for state in self.module.states:
        item_names = [x.item_name for x in state.item_lists]
        if state.state_provider and self.item_name in item_names:
            result = prepend_router_configs(
                state.state_provider.create_router_configs(), result
            )

    return result


def _find_behavior(self, name):
    return R.find(lambda x: x.name == name)(self.behaviors)


def p_section_imports(self):
    result = []
    selection_bvr = _find_behavior(self, "selection")
    if selection_bvr:
        result.append("import { Selection } from 'skandha-mobx/Selection';")
        result.append("import { ClickToSelectItems } from 'skandha-facets/handlers';")

    if _find_behavior(self, "highlight"):
        result.append("import { Highlight } from 'skandha-mobx/Highlight';")

    return "\n".join(result)


def p_section_default_props(self):
    result = []
    selection_bvr = _find_behavior(self, "selection")
    if selection_bvr:
        result.extend([f"          {self.items_name}Selection: Selection,"])
        result.extend(
            [f"          {self.items_name}HandlerClicks: ClickToSelectItems,"]
        )

    if _find_behavior(self, "highlight"):
        result.extend([f"          {self.items_name}Highlight: Highlight,"])

    return "\n".join(result)


def p_section_classnames(self):
    result = []
    if _find_behavior(self, "selection"):
        result.extend(
            [
                f"          '{self.name}Item--selected':",
                f"            x && props.{self.items_name}Selection.ids.includes(x.id),",  # noqa
            ]
        )

    if _find_behavior(self, "highlight"):
        result.extend(
            [
                f"          '{self.name}Item--highlighted':",
                f"            x && props.{self.items_name}Highlight.id == x.id,",  # noqa
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


def p_section_on_click(self):
    result = []
    if _find_behavior(self, "selection"):
        result.extend([f"          {{...props.{self.items_name}HandlerClicks}}"])
    else:
        result.extend(
            [f"          onClick={{() => alert('TODO: browse to {self.item_name}')}}"]
        )

    return "\n".join(result)
