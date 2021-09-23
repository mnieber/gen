import os

from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.magic_replace import magic_replace
from titan.react_module_pkg.apiquery.field_spec_to_ts_type import field_spec_to_ts_type

load_data_template = """
    if (queryName === 'getYellowTulips') {
      if (isUpdatedRS(rs)) {
        this.addYellowTulips(values(data.yellowTulips));
      }
      rsMap.registerRS(rs, [resUrls.yellowTulipById]);
    }
"""


class Sections:
    def __init__(self, res):
        self.res = res

    def item_list_fields(self):
        result = []
        for item_list in self.res.item_lists:
            result.append(
                f"  @observable {item_list.item_name}ById: "
                + f"{upper0(item_list.item_name)}ByIdT = {{}};\n"
            )
        return os.linesep.join(result)

    def on_load_data(self):
        result = ""
        for item_list in self.res.item_lists:
            result += magic_replace(
                load_data_template,
                [("yellowTulip", item_list.item_name)],
            )
        return result

    def define_type(self, item_name):
        result = []
        result.append(f"export type YellowTulipT = {{")
        type_spec = type_spec_store().get(upper0(item_name))
        for field_spec in type_spec.field_specs:
            if field_spec.private:
                continue

            t = field_spec_to_ts_type(field_spec)
            result.append(f"  {field_spec.name}: {t};")
        result.append(f"}}")

        return "\n".join(result)

    def define_form_type(self, item_name):
        result = []
        return "\n".join(result)
