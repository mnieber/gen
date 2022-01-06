from moonleap import u0
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def get_context_admin(module):
    class Sections:
        def get_inline_models(self, item_list):
            type_spec = ml_type_spec_from_item_name(item_list.item_name)
            return [
                u0(item_list.item_name) + "2" + u0(x.target)
                for x in type_spec.get_field_specs(["fk"])
                if x.through
            ]

        def admin_types(self, item_list):
            return ""

        def admin_body(self, item_list):
            inline_models = self.get_inline_models(item_list)
            if not inline_models:
                return "pass"
            return (
                "inlines = (" + ", ".join([x + "Inline," for x in inline_models]) + ")"
            )

    return dict(sections=Sections())
