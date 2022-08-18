def get_helpers(_):
    class Helpers:
        item_view = _.component
        type_spec = item_view.item.type_spec

        @property
        def fields(self):
            result = []

            for field_spec in self.type_spec.get_field_specs():
                if not (
                    "client" not in field_spec.api
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    result.append(field_spec)

            return result

    return Helpers()
