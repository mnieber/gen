from moonleap.typespec.type_spec_store import type_spec_store
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type


def get_context(item_type):
    _ = lambda: None

    class Sections:
        def define_type(self):
            result = []

            result.append(f"export type {item_type.ts_type} = {{")
            for field_spec in item_type.type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                postfix = "Id" if field_spec.field_type == "fk" else ""
                result.append(f"  {field_spec.name}{postfix}: {t};")
            result.append(f"}};")

            return "\n".join(result)

        def define_form_type(self):
            if not item_type.form_type:
                return ""

            result = []
            result.append(f"export type {item_type.ts_form_type} = {{")

            form_type_spec = type_spec_store().get(item_type.form_type.name, None)
            for field_spec in form_type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                result.append(f"  {field_spec.name}: {t};")

            result.append(r"};")

            return "\n".join(result)

    return dict(sections=Sections(), _=_)
