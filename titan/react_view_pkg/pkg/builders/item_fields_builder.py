import copy

from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin


class ItemFieldsBuilder(BuilderItemsMixin, Builder):
    def create_widget_class_name(self):
        return self.parent_builder.create_widget_class_name()

    def build(self, div_attrs=None):
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        child_widget_specs = []
        item_expr = self.item_expr()

        for field_spec in self.item.type_spec.get_field_specs():
            if "client" in field_spec.has_model and not field_spec.field_type in (
                "fk",
                "relatedSet",
            ):
                child_widget_spec = copy.deepcopy(field_widget_spec)
                child_widget_spec.values[
                    "field_expr"
                ] = f"{item_expr}.{field_spec.name}"
                child_widget_specs.append(child_widget_spec)

        self._add_child_widgets(child_widget_specs)


class ItemFieldBuilder(BuilderItemsMixin, Builder):
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
