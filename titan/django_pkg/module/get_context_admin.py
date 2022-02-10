def get_context_admin(module):
    class Sections:
        def get_inline_models(self, item_list):
            return [
                item_list.item_type.name + "2" + x.target
                for x in item_list.type_spec.get_field_specs(["relatedSet"])
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
