import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, kebab_to_camel, render_templates, rule, tags
from moonleap.verbs import has, loads
from moonleap_react_module.graphqlapi.__init__ import GraphqlApi

from . import props
from .resources import DataLoader


@tags(["dataloader"])
def create_dataloader(term, block):
    name = kebab_to_camel(term.data)
    dataloader = DataLoader(name=name)
    return dataloader


@extend(DataLoader)
class ExtendDataLoader:
    render = MemFun(render_templates(__file__))
    body = Prop(props.body)
    items = P.children(loads, "item")
    item_lists = P.children(loads, "item-list")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    dataloaders = P.children(has, "dataloaders")
