import os

from moonleap.utils.inflect import plural
from moonleap.utils.quote import quote
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
from titan.react_pkg.pkg.ts_var import (
    ts_form_type,
    ts_type,
    ts_type_import_path,
    ts_var,
    ts_var_by_id,
    ts_var_by_id_type,
)


def get_context(store):
    _ = lambda: None
    _.graphql_api = ml_graphql_api(ml_react_app(store))
    _.service = ml_react_app(store).service
    _.handled_queries = _.service.get_tweak_or(
        [], ["react_app", "stores", store.name, "handled_queries"]
    )
    _.ignored_queries = _.service.get_tweak_or(
        [], ["react_app", "stores", store.name, "ignored_queries"]
    )

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

        def prop_names(self):
            result = []
            for item_list in store.item_lists_stored:
                item_name = item_list.item_name
                result.append(quote(plural(item_name)))
            return ", ".join(result)

        def queries_handled(self):
            query_names = []

            for item_list in store.item_lists_stored:
                queries = list(_.graphql_api.queries)
                mutations = list(_.graphql_api.mutations)

                for query in queries + mutations:
                    output_field_specs = [
                        x
                        for x in query.outputs_type_spec.get_field_specs(
                            ["fk", "relatedSet"]
                        )
                        if x.target == item_list.item_name
                    ]

                    if output_field_specs or query.name in _.handled_queries:
                        query_names.append(quote(query.name))

            return ", ".join(query_names)

        def define_type(self, item):
            result = []
            type_spec = ml_type_spec_from_item_name(item.item_name)

            result.append(f"export type {ts_type(item)} = {{")
            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                postfix = "Id" if field_spec.field_type == "fk" else ""
                result.append(f"  {field_spec.name}{postfix}: {t};")
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
