from moonleap import u0
from moonleap.utils.inflect import plural
from titan.react_pkg.pkg.ts_var import ts_type_from_item_name
from titan.react_view_pkg.router import RouterConfig


def get_select_item_effect_route_params(select_item_effect):
    params = [
        select_item_effect.item_list.item_name + u0(param)
        for param in select_item_effect.item_list.type_spec.select_item_by or []
    ]
    return params


def create_router_configs(self, named_component):
    return [
        RouterConfig(
            component=named_component,
            url="",
            params=get_select_item_effect_route_params(named_component.typ),
        )
    ]


def get_context(select_item_effect):
    _ = lambda: None
    _.item_list = select_item_effect.item_list
    _.item_name = _.item_list.item_name
    _.type_spec = _.item_list.type_spec
    _.items_name = plural(_.item_name)
    _.route_params = [
        _.item_name + u0(param) for param in _.type_spec.select_item_by or []
    ]

    class Sections:
        def select_effect_args(self):
            return ", ".join(
                [f"{route_param}: string" for route_param in _.route_params]
            )

        def declare_params(self):
            return "{ " + ", ".join(_.route_params) + " }"

        def extract_params(self):
            return ", ".join(
                [
                    f"{route_param}: params.{route_param}"
                    for route_param in _.route_params
                ]
            )

        def get_item_id(self):
            search_function = f"(x: {ts_type_from_item_name(_.item_name)}) => " + (
                " && ".join(
                    [
                        f"x.{param} === args.{_.item_name + u0(param)}"
                        for param in _.type_spec.select_item_by or []
                    ]
                )
                if _.route_params
                else "true"
            )

            return (
                ""
                if _.route_params == [f"{_.item_name}Id"]
                else f"const {_.item_name}Id = "
                + f"R.find({search_function})(args.{_.items_name})?.id"
            )

    return dict(sections=Sections(), _=_)
