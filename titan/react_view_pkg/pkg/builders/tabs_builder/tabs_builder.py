from pathlib import Path

from moonleap import get_tpl, u0
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg


class TabsBuilder(Builder):
    def build(self):
        self.use_uniform_height = bool(self.widget_spec.values.get("uniformHeight"))
        self.widget_class_name = self.widget_spec.root.widget_class_name
        context = dict(__=self._get_context())
        context["__"]["tab_instance_div"] = self.output.graft(
            self._get_tab_instance_output(self.widget_class_name + "__Tab")
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_context(self):
        type_spec = get_type_reg().get(u0(self.ilh.working_item_name))

        return {
            "item_name": self.ilh.working_item_name,
            "items_expr": self.ilh.item_list_data_path(),
            "component_name": self.widget_class_name,
            "display_field_name": (
                type_spec.display_field.name if type_spec.display_field else None
            ),
            "uniform_tab_height": self.use_uniform_height,
        }

    def get_spec_extension(self, places):
        extension = {}
        if not self.ilh.maybe_add_items_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no items pipeline")
        return extension

    def _get_tab_instance_output(self, tab_cn):
        # This returns the div that is used in the Tabs.
        # Don't confuse this with the div that is used in the TabsItem.
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        child_widget_spec = self.widget_spec.get_place("Tab")
        with child_widget_spec.memo(["div"]):
            item_name = self.ilh.working_item_name
            child_widget_spec.div.key = f"{item_name}.id"
            if self.use_uniform_height:
                child_widget_spec.div.append_styles(
                    [f'"{tab_cn}"', f"idx === {item_name}Idx ? 'visible' : 'invisible'"]
                )
            return build_widget_spec(child_widget_spec)
