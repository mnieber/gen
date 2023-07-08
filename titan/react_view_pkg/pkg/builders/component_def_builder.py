from moonleap import append_uniq, kebab_to_camel, u0
from titan.react_view_pkg.pkg.builder import Builder


class ComponentDefBuilder(Builder):
    def build(self):
        self.output.add(
            imports=(_get_prop_import_paths(self.widget_spec)),
            props=_get_props_lines(self.widget_spec),
            default_props=_get_default_props(self.widget_spec),
        )


def _get_prop_import_paths(widget_spec):
    result = []
    for named_prop in widget_spec.named_props:
        t = named_prop.meta.term
        if t.tag in ("item", "item~list"):
            type_name = u0(kebab_to_camel(t.data))
            append_uniq(
                result,
                f"import {{ { type_name }T }} from '/src/api/types/{ type_name }T';",
            )
    return result


def _get_props_lines(widget_spec):
    result = []
    for named_prop in widget_spec.named_props:
        result += [f"{named_prop.typ.ts_var}: {named_prop.typ.ts_type};"]
    return result


def _get_default_props(widget_spec):
    result = []
    for named_prop in widget_spec.named_default_props:
        append_uniq(result, named_prop.typ.ts_var)
    return result
