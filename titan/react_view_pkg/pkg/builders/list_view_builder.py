from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder

from .list_view_builder_tpl import imports_tpl, instance_tpl, preamble_tpl, props_tpl
from .lvi_builder_tpl import lvi_props_tpl


def default_spec(lvi_name, item_term_str):
    return {
        f"ListViewItem with {lvi_name} as Bar[p-2]": {
            "__attrs__": f"item={item_term_str}",
            "LeftSlot with LviFields": "pass",
            "RightSlot with LviButtons": "pass",
        }
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
            return default_spec(
                lvi_name=f"{ self.item_name }-list-view-item:view",
                item_term_str=f"+{self.item_name}:item",
            )

    def build(self):

        extend_uniq(
            self.output.default_props,
            []
            + ([f"{self.items_name}:selection"] if self.has_selection else [])
            + ([f"{self.items_name}:highlight"] if self.has_highlight else [])
            + ([f"{self.items_name}:drag-and-drop"] if self.has_drag_and_drop else [])
            + ([f"{self.items_name}:deletion"] if self.has_deletion else []),
        )

        context = {
            "item_name": self.item_name,
            "items_expr": self.item_list_data_path(),
            "selection_bvr": self.has_selection,
            "highlight_bvr": self.has_highlight,
            "drag_and_drop_bvr": self.has_drag_and_drop,
            "deletion_bvr": self.has_deletion,
        }

        self.add_import_lines(
            [self.render_str(imports_tpl, context, "list_view_builder_imports.j2")]
        )

        # Add preamble
        if True:
            builder_output = self._get_child_widget_div(context)
            context["child_widget_div"] = builder_output.div
            self.add_preamble_lines(
                [
                    self.render_str(
                        preamble_tpl, context, "list_view_builder_preamble.j2"
                    )
                ]
            )
            # Add the rest of the builder_output that we haven't used so far
            # (especially child_components)
            builder_output.clear_div_lines()
            self.output.add(builder_output)

        self.add_lines(
            [self.render_str(instance_tpl, context, "list_view_builder_instance.j2")]
        )

    def _get_child_widget_div(self, context):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        child_widget_spec = self.widget_spec.find_child_with_place("ListViewItem")
        memo = child_widget_spec.create_memo()

        child_widget_spec.div_key = f"{self.item_name}.id"
        props = self.render_str(props_tpl, context, "list_view_builder_props.j2")
        child_widget_spec.div_props += [props]

        builder = get_builder(child_widget_spec, is_instance=True)
        builder.build()

        child_widget_spec.restore_memo(memo)

        return builder.output

    def update_place(self, widget_spec):
        if widget_spec.place == "ListViewItem":
            context = {
                "selection_bvr": self.has_selection,
                "highlight_bvr": self.has_highlight,
                "drag_and_drop_bvr": self.has_drag_and_drop,
                "deletion_bvr": self.has_deletion,
            }

            append_uniq(
                widget_spec.div_props,
                self.render_str(lvi_props_tpl, context, "lvi_body_builder_props.j2"),
            )
