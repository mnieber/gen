import os

from moonleap import u0
from moonleap.render.process_lines import process_lines
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
from titan.react_state_pkg.behavior.props import Sections as BehaviourSections


def get_delete_function_name(graphql_api, item_name):
    for mutation in graphql_api.mutations:
        for item_list in mutation.item_lists_deleted:
            if item_list.item_name == item_name:
                return mutation.name

    raise Exception(f"Could not find mutation that deletes {item_name}")


class Sections(BehaviourSections):
    def __init__(self, res):
        self.res = res
        self.graphql_api = ml_graphql_api(ml_react_app(res.state))
        self.delete_function_name = get_delete_function_name(
            self.graphql_api, res.item_name
        )

    def imports(self):
        result = super().imports()
        return (
            result
            + os.linesep
            + f"import {{ {self.delete_function_name} }} from "
            + f"'src/api/mutations/{self.delete_function_name}';"
        )

    def callbacks(self, bvrs):
        return process_lines(
            {
                101: r"setCallbacks(ctr.deletion, {",
                102: r"  delete: {",
                103: r"    deleteItems(this: DeletionCbs['delete']) {",
                104: f"      return {self.delete_function_name}(this.itemIds);",
                105: r"    },",
                106: r"  },",
                107: r"} as DeletionCbs);",
            },
            remove={},
            indent=4,
        )

    def policies(self, bvrs):
        return r"// deletion (empty)"

    def default_props(self, store):
        indent = "      "
        result = [
            f"{self.res.items_name}Deletion: () => state.{self.res.items_name}.deletion,",  # noqa: E501
        ]
        return os.linesep.join([(indent + x) for x in result]) + os.linesep
