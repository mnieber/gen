import os

from moonleap import u0
from moonleap.utils.fp import uniq
from moonleap.utils.inflect import plural
from moonleap.utils.quote import quote
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.api_pkg.typeregistry import TypeRegistry
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


def _get_related_set_field_specs_by_list_item_name(store):
    result = dict()
    for item_list in store.item_lists_stored:
        item_name = item_list.item_name
        result[item_name] = []
        for field_spec in ml_type_spec_from_item_name(item_name).get_field_specs(
            ["relatedSet"]
        ):
            if not field_spec.private and field_spec not in result[item_name]:
                result[item_name].append(field_spec)
    return result


def _get_targets(store, related_set_field_specs_by_list_item_name):
    result = [item_list.item_name for item_list in store.item_lists_stored]
    for (
        list_item_name,
        related_set_field_specs,
    ) in related_set_field_specs_by_list_item_name.items():
        result.extend(
            [
                related_set_field_spec.target
                for related_set_field_spec in related_set_field_specs
            ]
        )
    return result


def get_context(store):
    _ = lambda: None
    _.graphql_api = ml_graphql_api(ml_react_app(store))
    _.type_reg = TypeRegistry(_.graphql_api)
    _.service = ml_react_app(store).service
    _.handled_queries = _.service.get_tweak_or(
        [], ["react_app", "stores", store.name, "handled_queries"]
    )
    _.ignored_queries = _.service.get_tweak_or(
        [], ["react_app", "stores", store.name, "ignored_queries"]
    )
    _.related_set_field_specs_by_list_item_name = (
        _get_related_set_field_specs_by_list_item_name(store)
    )
    _.targets = _get_targets(store, _.related_set_field_specs_by_list_item_name)

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
                for field_spec in _.related_set_field_specs_by_list_item_name.get(
                    item_list.item_name, []
                ):
                    item = _.type_reg.get_item_by_name(field_spec.target)
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

            for (
                list_item_name,
                related_set_field_specs,
            ) in _.related_set_field_specs_by_list_item_name.items():
                for related_set_field_spec in related_set_field_specs:
                    fk_item_name = related_set_field_spec.target
                    result.append(quote(plural(fk_item_name)))
                    result.append(quote(f"deleted{u0(fk_item_name)}Ids"))

            return ", ".join(uniq(result))

        def queries_handled(self):
            query_names = []
            queries = list(_.graphql_api.queries)
            mutations = list(_.graphql_api.mutations)

            for query in queries + mutations:
                query_returns_a_target = [
                    x
                    for x in query.outputs_type_spec.get_field_specs(
                        ["fk", "relatedSet"]
                    )
                    if x.target in _.targets
                ]
                query_deletes_a_target = [
                    x
                    for x in getattr(query, "item_lists_deleted", [])
                    if x.item_name in _.targets
                ]
                if (
                    query.name in _.handled_queries
                    or query_returns_a_target
                    or query_deletes_a_target
                ):
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

    return dict(sections=Sections(), _=_)
