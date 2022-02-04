from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type
from titan.react_pkg.pkg.ts_var import ts_form_type, ts_type


def get_context(item_type):
    _ = lambda: None

    class Sections:
        def define_type(self):
            result = []
            type_spec = ml_type_spec_from_item_name(item_type.name)

            result.append(f"export type {ts_type(item_type)} = {{")
            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                postfix = "Id" if field_spec.field_type == "fk" else ""
                result.append(f"  {field_spec.name}{postfix}: {t};")
            result.append(f"}}")

            return "\n".join(result)

        def define_form_type(self):
            if not item_type.form_type:
                return ""

            type_spec = ml_form_type_spec_from_item_name(item_type.name)

            result = []
            result.append(f"export type {ts_form_type(item_type)} = {{")

            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                result.append(f"  {field_spec.name}: {t};")

            result.append(r"}")

            return "\n".join(result)

    return dict(sections=Sections(), _=_)
