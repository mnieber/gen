import typing as T
from dataclasses import dataclass, field

from moonleap.resource import Resource
from titan.project_pkg.service import Tool


class ReactApp(Tool):
    pass


@dataclass
class ReactAppConfig(Resource):
    flags: T.Dict[str, T.Union[str, bool]] = field(default_factory=dict)
    index_imports: str = ""
    index_body: str = ""


def find_module_that_provides_item_list(react_app, item_name):
    for module in react_app.modules:
        for store in module.stores:
            for item_list in store.item_lists:
                if item_list.item_name == item_name:
                    return module
    return None
