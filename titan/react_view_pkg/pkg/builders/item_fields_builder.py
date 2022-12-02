import copy

from titan.react_view_pkg.pkg.builder import Builder
from titan.widgets_pkg.pkg.load_widget_specs.widget_spec_parser import WidgetSpecParser
from titan.widgets_pkg.pkg.widget_spec import WidgetSpec
from titan.widgets_pkg.widgetregistry.resources import WidgetRegistry

default_widget_spec = {"Field with Card": {"ItemField": "pass"}}


class ItemFieldsBuilder(Builder):
    def create_widget_class_name(self):
        return self.parent_builder.create_widget_class_name()

    def build(self, div_attrs=None):
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        if not field_widget_spec:
            widget_reg = WidgetRegistry()
            parser = WidgetSpecParser(widget_reg)
            field_widget_spec = parser.parse(default_widget_spec)[0]

        child_widget_specs = []
        item_expr = self.item_expr()

        for field_spec in self.item.type_spec.get_field_specs():
            if (
                "client" in field_spec.has_model
                and not field_spec.field_type
                in (
                    "slug" "fk",
                    "relatedSet",
                )
                and not (field_spec.name in ("id",))
            ):
                child_widget_spec = copy.deepcopy(field_widget_spec)
                child_widget_spec.values[
                    "field_expr"
                ] = f"{item_expr}.{field_spec.name}"
                child_widget_specs.append(child_widget_spec)

        self._add_child_widgets(child_widget_specs)


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
