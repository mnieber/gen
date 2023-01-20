from moonleap import u0
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg


class ItemFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            layout = "Card" if self.widget_spec.values.get("card") else "Div"
            return {f"Field with {layout}[cn=__]": {"ItemField": "pass"}}

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
        self.display_only = self.widget_spec.values.get("display")

        field_widget_spec = self.widget_spec.get_place("Field")
        for field_spec in self.get_field_specs():
            field_widget_spec.values["field_spec"] = field_spec
            self._add_child_widgets([field_widget_spec])


class ItemFieldBuilder(Builder):
    def build(self):
        item_data_path = self.ih.item_data_path()
        field_spec = self.widget_spec.get_value_by_name("field_spec", recurse=True)
        assert field_spec
        label = f"{field_spec.name}: " if field_spec.field_type in ("boolean",) else ""
        postfix = " ? 'Yes' : 'No'" if field_spec.field_type in ("boolean",) else ""
        field_expr = f"{item_data_path}.{field_spec.name}"
        self.output.add(lines=[f"{label}{{{field_expr}{postfix}}}"])
