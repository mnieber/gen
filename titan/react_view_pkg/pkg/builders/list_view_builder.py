from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder

from .list_view_builder_tpl import (
    lvi_imports_tpl,
    lvi_instance_props_tpl,
    lvi_instance_tpl,
    lvi_preamble_tpl,
)
from .lvi_builder_tpl import lvi_handler_props_tpl


def auto_spec(lvi_name, item_term_str):
    return {
        f"ListViewItem with {lvi_name}": "pass",
        f"{lvi_name} as Bar[p-2]": {
            "__attrs__": f"item={item_term_str}",
            "LeftSlot with LviFields": "pass",
            "RightSlot with LviButtons": "pass",
        },
    }


class ListViewBuilder(Builder):
    def __post_init__(self):
        self.item_name = self.named_item_list_term.data
        self.items_name = plural(self.item_name)
        self.bvrs = self.get_value_by_name("bvrs", "").split(",")
        self.has_selection = "selection" in self.bvrs
        self.has_highlight = "highlight" in self.bvrs
        self.has_drag_and_drop = "dragAndDrop" in self.bvrs
        self.has_deletion = "deletion" in self.bvrs

    def get_spec_extension(self, places):
        if "ListViewItem" not in places:
            return auto_spec(
                lvi_name=f"{ self.item_name }-list-view-item:view",
                item_term_str=f"+{self.item_name}:item",
            )

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = {
            "item_name": self.item_name,
            "items_expr": self.item_list_data_path(),
            "selection_bvr": self.has_selection,
            "highlight_bvr": self.has_highlight,
            "drag_and_drop_bvr": self.has_drag_and_drop,
            "deletion_bvr": self.has_deletion,
        }

        # Add imports
        self.add_import_lines(
            [self.render_str(lvi_imports_tpl, context, "liv__imports.j2")]
        )

        # Add preamble
        if True:
            builder_output = _get_lvi_instance_div(
                self.widget_spec,
                div_attrs=self.render_str(
                    lvi_instance_props_tpl, context, "lvi_div_attrs.j2"
                ),
                key=f"{self.item_name}.id",
            )
            context["child_widget_div"] = builder_output.div
            preamble_str = self.render_str(lvi_preamble_tpl, context, "lvi_preamble.j2")
            self.add_preamble_lines([preamble_str])

            # Add the rest of the builder_output that we haven't used so far
            # (especially the import_lines)
            builder_output.clear_div_lines()
            self.output.add(builder_output)

        # Add instance
        instance_str = self.render_str(lvi_instance_tpl, context, "lvi_instance.j2")
        self.add_lines([instance_str])

    def _add_default_props(self):
        extend_uniq(
            self.output.default_props,
            []
            + ([f"{self.items_name}:selection"] if self.has_selection else [])
            + ([f"{self.items_name}:highlight"] if self.has_highlight else [])
            + ([f"{self.items_name}:drag-and-drop"] if self.has_drag_and_drop else [])
            + ([f"{self.items_name}:deletion"] if self.has_deletion else []),
        )

    def update_place(self, widget_spec):
        if widget_spec.place == "ListViewItem":
            # Here we add extra props to the div of the ListViewItem definition.
            # Don't confuse this with the div of the ListViewItem instance.
            context = {
                "selection_bvr": self.has_selection,
                "highlight_bvr": self.has_highlight,
                "drag_and_drop_bvr": self.has_drag_and_drop,
                "deletion_bvr": self.has_deletion,
            }

            append_uniq(
                widget_spec.div_attrs,
                self.render_str(
                    lvi_handler_props_tpl, context, "lvi_body_builder_div_attrs.j2"
                ),
            )


def _get_lvi_instance_div(widget_spec, div_attrs, key):
    # This returns the div that is used in the ListView.
    # Don't confuse this with the div that is used in the ListViewItem.
    from titan.react_view_pkg.pkg.get_builder import get_builder

    child_widget_spec = widget_spec.find_child_with_place("ListViewItem")
    memo = child_widget_spec.create_memo()

    child_widget_spec.div_key = key
    child_widget_spec.div_attrs += [div_attrs]

    builder = get_builder(child_widget_spec, is_instance=True)
    builder.build()

    child_widget_spec.restore_memo(memo)

    return builder.output
