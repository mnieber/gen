def get_helpers(_):
    class Helpers:
        item_view = _.component
        type_spec = item_view.item.type_spec

        @property
        def fields(self):
            result = []

            for field_spec in self.type_spec.get_field_specs():
                if (
                    "client" in field_spec.has_model
                    and field_spec.name not in ("id",)
                    and field_spec.field_type not in ("slug", "fk", "relatedSet")
                ):
                    result.append(field_spec)

            return result

    return Helpers()
