import os

from moonleap import u0
from moonleap.utils.codeblock import CodeBlock
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

        def on_load_data(self):
            root = CodeBlock(style="typescript", level=2)

            for item_list in store.item_lists_stored:
                queries = list(_.graphql_api.queries)
                mutations = list(_.graphql_api.mutations)
                item_name = item_list.item_name
                items = plural(item_name)
                query_names = []

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

                root.abc(
                    r"const ignoredQueries = "
                    + f"[{', '.join([quote(x) for x in _.ignored_queries])}];"
                )
                root.abc(r"if (ignoredQueries.includes(queryName)) return;")
                root.abc("")

                root.abc(f"const handledQueries = [{', '.join(query_names)}];")
                root.abc(f"if (handledQueries.includes(queryName)) {{")
                root.abc(f"  if (isUpdatedRS(rs)) {{")
                root.abc(f"    if (!data.{items}) {{")
                root.IxI(
                    f"      console.warn",
                    [
                        f"`The query ${{queryName}} was handled in {store.name} ` +"
                        + f"'but does not return any {items}.'"
                    ],
                    "",
                )
                root.abc(r"    }")
                root.IxI(f"    this.add{u0(items)}", [f"values(data.{items})"], ";")
                root.abc(r"  }")
                root.abc(r"}")
                root.abc(f"else if (data?.{items}) {{")
                root.IxI(f"  this.add{u0(items)}", [f"values(data.{items})"], ";")
                root.IxI(
                    f"  console.warn",
                    [
                        f"`The query ${{queryName}} returned {items} but was not ` +"
                        + f"'explicitly handled in {store.name}. Please add a handler.'",
                    ],
                    "",
                )
                root.abc(f"}}")
                root.abc(f"rsMap.registerRS(rs, [resUrls.{item_name}ById]);")
            return root.result

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
