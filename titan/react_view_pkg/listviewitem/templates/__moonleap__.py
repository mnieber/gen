import ramda as R

from moonleap.utils import yaml2dict
from titan.react_view_pkg.pkg.list_view_item_builder import ListViewItemBuilder
from titan.widgets_pkg.pkg.load_widget_specs.widget_spec_parser import WidgetSpecParser
from titan.widgets_pkg.widgetregistry import get_widget_reg


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.list_view.bvrs)

    class Helpers:
        component_name = _.component.name
        item_kebab_name = _.component.list_view.item.kebab_name
        widget_spec = _.component.widget_spec
        type_spec = _.component.list_view.item.type_spec
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("deletion")
        drag_and_drop_bvr = _find_behavior("dragAndDrop")

        has_selection = selection_bvr
        has_highlight = selection_bvr or highlight_bvr
        has_drag_and_drop = drag_and_drop_bvr

        _build = None

        @property
        def build(self):
            if self._build is None:
                if not self.widget_spec:
                    default_lvi_spec = yaml2dict(
                        _.render("__moonleap__/DefaultListViewItemSpec.yaml.j2")
                    )
                    parser = WidgetSpecParser(get_widget_reg())
                    parser.parse(default_lvi_spec)
                    self.widget_spec = _.component.widget_spec

                builder = ListViewItemBuilder(
                    self.widget_spec, None, level=0, helpers=self, render=_.render
                )
                builder.build()
                self._build = builder.output
            return self._build

        @property
        def fields(self):
            result = []
            for field_spec in self.type_spec.get_field_specs():
                if (
                    "client" in field_spec.has_model
                    and field_spec.name not in ("id",)
                    and field_spec.field_type not in ("slug", "fk", "relatedSet")
                ):
                    result.append(field_spec)

            return result

    return Helpers()
