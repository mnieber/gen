from moonleap import u0
from moonleap.utils.fp import append_uniq, extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin
from titan.types_pkg.typeregistry import get_type_reg

from .tabs_builder_tpl import tpls


class TabsBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _add_lines(self):
        context = dict(__=self._get_context())
        context["__"]["tab_instance_div"] = self.output.graft(
            _get_tab_instance_output(
                self.widget_spec,
                div_attrs=None,
                key=f"{self.bvrs_item_name}.id",
            )
        )

        self.add(
            imports_lines=[tpls.render("tab_view_imports_tpl", context)],
            preamble_lines=[tpls.render("tab_view_preamble_tpl", context)],
            lines=[tpls.render("tab_view_div_tpl", context)],
        )

    def _get_context(self):
        type_spec = get_type_reg().get(u0(self.bvrs_item_name))

        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "items_expr": self.item_list_data_path(),
            "component_name": self.widget_spec.widget_class_name,
            "display_field_name": (
                type_spec.display_field.name if type_spec.display_field else None
            ),
            "uniform_tab_height": bool(
                self.widget_spec.get_value_by_name("uniformHeight")
            ),
        }


def _get_tab_instance_output(widget_spec, div_attrs, key):
    # This returns the div that is used in the Tabs.
    # Don't confuse this with the div that is used in the TabsItem.
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Tab")
    with child_widget_spec.memo():
        child_widget_spec.div_key = key
        if div_attrs:
            append_uniq(child_widget_spec.div_attrs, div_attrs)
        return build(child_widget_spec)
