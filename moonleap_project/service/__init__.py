import moonleap.resource.props as P
from moonleap import (
    StoreOutputPaths,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
)
from moonleap.parser.term import word_to_term
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.resource.rel import Rel
from moonleap.verbs import has, runs, uses
from moonleap_tools.tool import Tool

from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=kebab_to_camel(term.data), use_default_config=True)
    service.output_path = service.name + "/"
    # service.doc_meta.private_rel(
    #     Rel(word_to_term("service"), has, word_to_term(":tool"))
    # )
    return service


@rule("service", uses, "port")
def service_uses_port(service, port):
    service.port = port.term.data


@rule("service", uses + runs + has, "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
    return create_forward(
        service,
        has,
        ":tool",
        subj_res=service,
        obj_res=tool,
    )


@extend(Service)
class ExtendService(
    StoreOutputPaths,
    StoreTemplateDirs,
):
    src_dir = P.child(has, "src-dir")
