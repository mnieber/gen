from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags

from .resources import DataLoader


@tags(["dataloader"])
def create_dataloader(term, block):
    name = kebab_to_camel(term.data)
    dataloader = DataLoader(name=name)
    return dataloader


@extend(DataLoader)
class ExtendDataLoader:
    render = MemFun(render_templates(__file__))
