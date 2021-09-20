from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.magic_replace import magic_replace
from titan.react_module_pkg.apimodule.utils import field_spec_to_ts_type

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
        result = ""
        for item_list in self.res.item_lists:
            result += (
                f"  @observable {item_list.item_name}ById: "
                + f"{upper0(item_list.item_name)}ByIdT = {{}};\n"
            )
        return result

    def on_load_data(self):
        result = ""
        for item_list in self.res.item_lists:
            result += magic_replace(
                load_data_template,
                [("yellowTulip", item_list.item_name)],
            )
        return result

    def item_fields(self, item_type):
        result = []
        type_spec = type_spec_store().get(item_type.name)
        for field_spec in type_spec.field_specs:
            if field_spec.private:
                continue

            t = field_spec_to_ts_type(field_spec)
            result.append(f"  {field_spec.name}: {t};")

        return "\n".join(result)
