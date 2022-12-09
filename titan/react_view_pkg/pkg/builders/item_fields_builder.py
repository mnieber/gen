from moonleap import u0
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg


class ItemFieldsBuilder(Builder):
    def __post_init__(self):
        self.item_name = self.named_item_term.data
        self.type_spec = get_type_reg().get(u0(self.item_name))
        self.display_only = self.get_value_by_name("display")

    def get_spec_extension(self, places):
        if "Field" not in places:
            return {"Field with Card[cn=__]": {"ItemField": "pass"}}

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
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        item_data_path = self.item_data_path()
        for field_spec in self.get_field_specs():
            field_expr = f"{item_data_path}.{field_spec.name}"
            field_widget_spec.values["field_expr"] = field_expr
            self._add_child_widgets([field_widget_spec])


class ItemFieldBuilder(Builder):
    @property
    def field_expr(self):
        return self.get_value_by_name("field_expr")

    def build(self):
        self.add(lines=[f"{{{self.field_expr}}}"])
