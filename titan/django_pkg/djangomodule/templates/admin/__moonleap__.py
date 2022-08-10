import os

from moonleap.utils.case import sn
from moonleap.utils.quote import quote


def get_helpers(_):
    class Helpers:
        def get_inline_model_fields(self, item_list):
            return [
                x
                for x in item_list.type_spec.get_field_specs(["relatedSet"])
                if x.through and x.through != "+" and x.admin_inline
            ]

        def get_autocomplete_fields(self, type_spec):
            return [
                quote(sn(x.name))
                for x in type_spec.get_field_specs(["relatedSet"])
                if (not x.through or x.through == "+")
                and x.target_type_spec.admin_search_by
            ]

        def admin_types(self, item_list):
            return ""

        def admin_body(self, item_list):
            inline_model_fields = self.get_inline_model_fields(item_list)
            autocomplete_fields = self.get_autocomplete_fields(item_list.type_spec)
            admin_search_by = [quote(x) for x in item_list.type_spec.admin_search_by]

            if (
                not inline_model_fields
                and not admin_search_by
                and not autocomplete_fields
            ):
                return "    pass"

            result = []
            if inline_model_fields:
                result.append(
                    "    inlines = ("
                    + ", ".join(
                        [
                            item_list.item_type.name + x.target + "Inline"
                            for x in inline_model_fields
                        ]
                    )
                    + ",)"
                )
            if admin_search_by:
                result.append(
                    "    search_fields = (" + ", ".join(admin_search_by) + ",)"
                )
            if autocomplete_fields:
                result.append(
                    "    autocomplete_fields = ("
                    + ", ".join(autocomplete_fields)
                    + ",)"
                )

            return os.linesep.join(result)

        def inline_model_autocomplete_fields(self, inline_model_field):
            autocomplete_fields = self.get_autocomplete_fields(
                inline_model_field.target_type_spec
            )
            if not autocomplete_fields:
                return ""
            return "autocomplete_fields = (" + ", ".join(autocomplete_fields) + ",)"

    return Helpers()
