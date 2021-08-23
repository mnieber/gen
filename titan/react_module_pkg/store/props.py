from moonleap import upper0
from moonleap.resources.data_type_spec_store import FK, RelatedSet, data_type_spec_store
from moonleap.utils.magic_replace import magic_replace

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
        spec = data_type_spec_store.get_spec(item_type.name)
        for field in spec.fields:
            if field.private:
                continue

            t = field.field_type
            t = "string" if (isinstance(t, FK) or isinstance(t, RelatedSet)) else t
            result.append(f"  {field.name}: {t};")

        return "\n".join(result)
