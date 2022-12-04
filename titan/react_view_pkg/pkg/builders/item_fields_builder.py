import copy

from titan.react_view_pkg.pkg.builder import Builder
from titan.widgets_pkg.pkg.load_widget_specs.widget_spec_parser import WidgetSpecParser

default_widget_spec = {"Field with Card[cn=__]": {"ItemField": "pass"}}


class ItemFieldsBuilder(Builder):
    def get_field_specs(self):
        type_spec = self.item.type_spec
        skip_list = ("slug", "fk", "relatedSet")
        return [
            field_spec
            for field_spec in type_spec.get_field_specs()
            if (
                "client" in field_spec.has_model
                and not field_spec.field_type in skip_list
                and not (field_spec.name in ("id",))
            )
        ]

    def build(self, div_attrs=None):
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        if not field_widget_spec:
            parser = WidgetSpecParser()
            field_widget_spec = parser.parse(
                default_widget_spec, parent_widget_spec=self.widget_spec
            )[0]
            field_widget_spec.place = "Field"

        item_data_path = self.item_data_path()
        for field_spec in self.get_field_specs():
            field_expr = f"{item_data_path}.{field_spec.name}"
            field_widget_spec.values["field_expr"] = field_expr
            self._add_child_widgets([field_widget_spec])


class ItemFieldBuilder(Builder):
    @property
    def field_expr(self):
        b = self
        while b:
            if "field_expr" in b.widget_spec.values:
                return b.widget_spec.values["field_expr"]
            b = b.parent_builder
        raise Exception("field_expr not found")

    def build(self, div_attrs=None):
        self.add_lines([f"{{{self.field_expr}}}"])
