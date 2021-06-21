from moonleap import upper0
from moonleap.utils.magic_replace import magic_replace

load_data_template = """
    if (queryName === 'loadYellowTulips') {
      if (isUpdatedRS(state)) {
        this.yellowTulipById = event.payload.yellowTulips;
      }
      rsStore.registerState(state, [resourceUrls.yellowTulips]);
    }
"""


def construct_item_lists_section(self):
    result = ""
    for item_list in self.item_lists:
        result += (
            f"  {item_list.item_name}ById: "
            + f"{upper0(item_list.item_name)}ByIdT = {{}};\n"
        )
    return result


def on_load_data_section(self):
    result = ""
    for item_list in self.item_lists:
        result += magic_replace(
            load_data_template,
            [("yellowTulip", item_list.item_name)],
        )
    return result
