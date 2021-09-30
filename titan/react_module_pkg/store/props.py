import os

import ramda as R
from moonleap.utils.magic_replace import magic_replace
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type
from titan.react_pkg.pkg.get_chain import get_chain_to
from titan.react_pkg.pkg.ts_var import (
    ts_form_type,
    ts_type,
    ts_type_import_path,
    ts_var,
    ts_var_by_id,
    ts_var_by_id_type,
)

items_loaded_template = """
    if (queryName === 'theQueryName') {
      if (isUpdatedRS(rs)) {
        this.addYellowTulips(values(data.yellowTulips));
      }
      rsMap.registerRS(rs, [resUrls.yellowTulipById]);
    }
"""

item_loaded_template = """
    if (queryName === 'theQueryName') {
      if (isUpdatedRS(rs)) {
        this.yellowTulip = data.yellowTulip;
      }
      rsMap.registerRS(rs, [resUrls.yellowTulip]);
    }
"""


def get_context(store):
    class Sections:
        def import_policies(self):
            if store.policies:
                return (
                    f"import * as Policies from '{store.module.module_path}/policies';"
                )
            return ""

        def import_item_types(self):
            result = []

            for item_list in store.item_lists_stored:
                item = item_list.item
                result.append(
                    f"import {{ {ts_type(item)}, {ts_var_by_id_type(item)} }} "
                    + f"from '{ts_type_import_path(item)}';"
                )

            for item in store.items_stored:
                result.append(
                    f"import {{ {ts_type(item)} }} "
                    + f"from '{ts_type_import_path(item)}';"
                )

            return os.linesep.join(result)

        def item_list_fields(self):
            result = []
            for item_list in store.item_lists_stored:
                result.append(
                    f"  @observable {ts_var_by_id(item_list.item)}: "
                    + f"{ts_var_by_id_type(item_list.item)} = {{}};\n"
                )
            return os.linesep.join(result)

        def item_fields(self):
            result = []
            for item in store.items_stored:
                result.append(
                    f"  @observable {ts_var(item)}: "
                    + f"{ts_type(item)} | undefined;\n"
                )
            return os.linesep.join(result)

        def on_load_data(self):
            result = ""

            for item_list in store.item_lists_stored:
                chain = get_chain_to(item_list, store)
                query = chain[0].subj if chain else None
                if query:
                    result += magic_replace(
                        items_loaded_template,
                        [
                            ("yellowTulip", item_list.item_name),
                            ("theQueryName", query.name),
                        ],
                    )

            for item in store.items_stored:
                chain = get_chain_to(item, store)
                query = chain[0].subj if chain else None
                result += magic_replace(
                    item_loaded_template,
                    [
                        ("yellowTulip", item.item_name),
                        ("theQueryName", query.name),
                    ],
                )
            return result

        def define_type(self, item):
            result = []
            type_spec = ml_type_spec_from_item_name(item.item_name)

            result.append(f"export type {ts_type(item)} = {{")
            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                result.append(f"  {field_spec.name}: {t};")
            result.append(f"}}")

            return "\n".join(result)

        def define_form_type(self, item):
            if not item.item_type.form_type:
                return ""

            type_spec = ml_form_type_spec_from_item_name(item.item_name)

            result = []
            result.append(f"export type {ts_form_type(item)} = {{")

            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                result.append(f"  {field_spec.name}: {t};")

            result.append(r"}")

            return "\n".join(result)

    return dict(sections=Sections())
