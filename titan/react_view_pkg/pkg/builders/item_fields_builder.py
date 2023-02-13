from moonleap import u0
from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg


class ItemFieldsBuilder(Builder):
    type = "ItemFields"

    def get_spec_extension(self, places):
        if "Field" not in places:
            layout = "Card" if self.get_value("card") else "Div"
            return {
                f"Field with {layout}": {
                    "__class__": "__",
                    "ItemField": "pass",
                }
            }

    def get_field_specs(self):
        skip_list = ("slug", "fk", "relatedSet")
        if self.display_only and self.type_spec.display_field:
            return [self.type_spec.display_field]
        return [
            field_spec
            for field_spec in self.type_spec.get_field_specs()
            if (
                "client" in field_spec.has_model
                and not field_spec.field_type in skip_list
                and not (field_spec.name in ("id",))
            )
        ]

    def build(self):
        self.type_spec = get_type_reg().get(u0(self.ih.working_item_name))
        self.display_only = self.get_value("display")

        field_widget_spec = self.widget_spec.get_place("Field")
        for field_spec in self.get_field_specs():
            field_widget_spec.set_value("field_spec", field_spec)
            add_child_widgets(self, [field_widget_spec])


class ItemFieldBuilder(Builder):
    type = "ItemField"

    def build(self):
        item_data_path = self.ih.item_data_path()
        field_spec = self.get_value("field_spec", recurse=True)
        assert field_spec
        label = f"{field_spec.name}: " if field_spec.field_type in ("boolean",) else ""
        postfix = " ? 'Yes' : 'No'" if field_spec.field_type in ("boolean",) else ""
        field_expr = f"{item_data_path}.{field_spec.name}"
        self.output.add(lines=[f"{label}{{{field_expr}{postfix}}}"])
