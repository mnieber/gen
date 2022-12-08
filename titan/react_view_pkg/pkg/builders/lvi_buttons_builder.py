from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .lvi_buttons_builder_tpl import (
    lvi_buttons_add_props_tpl,
    lvi_buttons_imports_tpl,
    lvi_buttons_preamble_tpl,
    lvi_buttons_props_tpl,
    lvi_buttons_tpl,
)


class LviButtonsBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        context = self._get_context()

        self.add(
            lines=[self.render_str(lvi_buttons_tpl, context, "lvi_buttons_tpl.j2")],
            import_lines=[
                self.render_str(
                    lvi_buttons_imports_tpl, context, "lvi_buttons_imports_tpl.j2"
                )
            ],
            preamble_lines=[
                self.render_str(
                    lvi_buttons_preamble_tpl, context, "lvi_buttons_preamble_tpl.j2"
                )
            ],
            props_lines=[
                self.render_str(lvi_buttons_props_tpl, context, "lvi_buttons_tpl.j2")
            ],
            add_props_lines=[
                self.render_str(
                    lvi_buttons_add_props_tpl, context, "lvi_buttons_add_props_tpl.j2"
                )
            ],
        )

    def update_widget_spec(self):
        pass

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "component_name": self.widget_spec.widget_class_name,
            "uikit": self.use_uikit,
        }
