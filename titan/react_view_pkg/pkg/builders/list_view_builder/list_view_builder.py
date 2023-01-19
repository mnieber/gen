from pathlib import Path

from moonleap.render.render_template.tpl import get_tpl
from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.merge_into_config import merge_into_config
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper

from .spec_ext import spec_ext


class ListViewBuilder(Builder):
    def build(self):
        self.bvrs_helper = BvrsHelper(self.widget_spec, self.ilh.working_item_name)
        self._add_default_props()
        self._add_lines()

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_helper.bvrs_default_props())

    def _get_context(self):
        return {
            **self.bvrs_helper.bvrs_context(),
            "__item_name": self.ilh.working_item_name,
            "__items_expr": self.ilh.item_list_data_path(),
            "update_url": self.widget_spec.values.get("updateUrl"),
        }

    def _add_lines(self):
        context = self._get_context()
        context["child_widget_div"] = self.output.graft(self._get_lvi_instance_output())
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_lvi_instance_output(self):
        # This returns the div that is used in the ListView.
        # Don't confuse this with the div that is used in the ListViewItem.
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        context = self._get_context()
        tpl_lvi_props = get_tpl(Path(__file__).parent / "tpl_lvi_props.tsx.j2", context)

        child_widget_spec = self.widget_spec.get_place("ListViewItem")
        with child_widget_spec.memo():
            key = f"{self.ilh.working_item_name}.id"
            child_widget_spec.div.key = key
            append_uniq(child_widget_spec.div.attrs, tpl_lvi_props.get_section("props"))
            return build_widget_spec(child_widget_spec)

    def get_spec_extension(self, places):
        extension = {}
        if not self.ilh.maybe_add_items_pipeline_to_spec_extension(extension):
            raise Exception("ListViewBuilder: no items pipeline")

        if not self.ilh.maybe_add_item_pipeline_to_spec_extension(
            "component:props", extension
        ):
            raise Exception("ListViewBuilder: no item pipeline")

        pipeline_data = (
            self.widget_spec.get_pipeline_data("item", recurse=True)
            or extension["__pipelines__"]["item"]
        )
        named_item_term_str = pipeline_data[-1]
        merge_into_config(extension, spec_ext(self, places, named_item_term_str))
        return extension
