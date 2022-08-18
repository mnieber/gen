from moonleap import u0
from moonleap.utils.inflect import plural


def get_helpers(_):
    select_item_effect = _.component
    _item_list = select_item_effect.item_list
    _item_name = _item_list.item_name

    class Helpers:
        item_list = _item_list
        item_name = _item_name
        type_spec = item_list.item.type_spec
        items_name = plural(item_name)
        route_params = [
            _item_name + u0(param) for param in type_spec.select_item_by or []
        ]

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
            search_function = f"(x: {self.item_list.item.ts_type}) => " + (
                " && ".join(
                    [
                        f"x.{param} === args.{self.item_name + u0(param)}"
                        for param in self.type_spec.select_item_by or []
                    ]
                )
                if self.route_params
                else "true"
            )

            return (
                ""
                if self.route_params == [f"{self.item_name}Id"]
                else f"const {self.item_name}Id = "
                + f"R.find({search_function})(args.{self.items_name})?.id"
            )

    return Helpers()
