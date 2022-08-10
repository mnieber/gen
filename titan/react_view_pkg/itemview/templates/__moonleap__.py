import os


def get_helpers(_):
    class Helpers:
        item_view = _.component
        type_spec = item_view.item.item_type.type_spec

        def fields(self):
            result = []

            for field_spec in self.type_spec.field_specs:
                if (
                    field_spec.private
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    continue

                if field_spec.field_type in ("boolean"):
                    value = f"props.{self.item_view.item_name}.{field_spec.name} ? 'Yes' : 'No'"
                else:
                    value = f"props.{self.item_view.item_name}.{field_spec.name}"

                result.append(f"<div>{field_spec.name}: {{{value}}}</div>")
            return os.linesep.join(" " * 6 + line for line in result)

    return Helpers()
