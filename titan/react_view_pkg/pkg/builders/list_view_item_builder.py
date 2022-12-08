from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .list_view_item_builder_tpl import (
    lvi_div_attrs_tpl,
    lvi_div_styles_tpl,
    lvi_imports_tpl,
    lvi_props_tpl,
)


class ListViewItemBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        context = self._get_context()

        self.add(
            import_lines=[
                self.render_str(lvi_imports_tpl, context, "lvi_imports_tpl.j2")
            ],
            props_lines=[self.render_str(lvi_props_tpl, context, "lvi_div_attrs.j2")],
        )

    def update_widget_spec(self):
        context = self._get_context()

        if not self.named_item_term:
            self.widget_spec.values["item"] = f"+{self.bvrs_item_name}:item"

        append_uniq(
            self.widget_spec.div_styles,
            self.render_str(lvi_div_styles_tpl, context, "lvi_div_styles.j2"),
        )
        append_uniq(
            self.widget_spec.div_attrs,
            self.render_str(lvi_div_attrs_tpl, context, "lvi_div_attrs.j2"),
        )

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "component_name": self.widget_spec.widget_class_name,
        }
