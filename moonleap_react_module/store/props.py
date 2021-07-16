from moonleap import upper0
from moonleap.utils.magic_replace import magic_replace

load_data_template = """
    if (queryName === 'getYellowTulips') {
      if (isUpdatedRS(rs)) {
        this.addYellowTulips(values(event.payload.data.yellowTulips));
      }
      rsMap.registerRS(rs, [resUrls.yellowTulipById]);
    }
"""


def p_section_item_list_fields(self):
    result = ""
    for item_list in self.item_lists:
        result += (
            f"  @observable {item_list.item_name}ById: "
            + f"{upper0(item_list.item_name)}ByIdT = {{}};\n"
        )
    return result


def p_section_on_load_data(self):
    result = ""
    for item_list in self.item_lists:
        result += magic_replace(
            load_data_template,
            [("yellowTulip", item_list.item_name)],
        )
    return result
