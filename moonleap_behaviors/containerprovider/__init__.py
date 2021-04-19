import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.utils.inflect import singular
from moonleap.verbs import has
from moonleap_behaviors.container.resources import Container

from . import props
from .resources import ContainerProvider


@tags(["container-provider"])
def create_container_provider(term, block):
    kebab_name = term.data
    items_name = kebab_to_camel(kebab_name)
    item_name = singular(items_name)
    container_provider = ContainerProvider(
        name=f"{items_name}CtrProvider", item_name=item_name
    )
    return container_provider


@rule("container")
def container_created(container):
    return create_forward(container, has, f"{container.name}:container-provider")


@rule("container", has, "container-provider")
def container_has_container_provider(container, container_provider):
    container_provider.output_paths.add_source(container)


@extend(Container)
class ExtendContainer:
    container_provider = P.child(has, "container-provider")


@extend(ContainerProvider)
class ExtendContainerProvider:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
