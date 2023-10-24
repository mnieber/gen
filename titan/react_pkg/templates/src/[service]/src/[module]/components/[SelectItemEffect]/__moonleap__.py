from moonleap import u0
from moonleap.utils.inflect import plural


def get_helpers(_):
    class Helpers:
        select_item_effect = _.component
        item_list = select_item_effect.item_list
        item_name = item_list.item_name
        type_spec = item_list.item.type_spec
        items_name = plural(item_name)
        route_params = []

        def __init__(self):
            self.route_params = []

        def select_effect_args(self):
            return ", ".join(
                [f"{route_param}: string" for route_param in self.route_params]
            )

        def declare_params(self):
            return "{ " + ", ".join(self.route_params) + " }"

        def extract_params(self):
            return ", ".join(
                [
                    f"{route_param}: params.{route_param}"
                    for route_param in self.route_params
                ]
            )

        def get_item_id(self):
            search_function = f"(x: {self.item_list.item.ts_type}) => true"
            return (
                ""
                if self.route_params == [f"{self.item_name}Id"]
                else f"R.find({search_function})(props.{self.items_name})?.id"
            )

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "SelectItemEffect.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "select-item-effect"
    ]
