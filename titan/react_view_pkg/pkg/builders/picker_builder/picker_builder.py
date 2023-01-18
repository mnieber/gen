from pathlib import Path

from moonleap import get_tpl
from moonleap.utils.fp import extend_uniq
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper


class PickerBuilder(Builder):
    def build(self):
        self.bvrs_helper = self._get_bvrs_helper()
        self._add_packages()
        self._add_default_props()
        self._add_lines()

    def _get_bvrs_helper(self):
        bvrs_helper = BvrsHelper(self.widget_spec, self.ilh.working_item_name)
        if bvrs_helper.bvrs_has_selection and not bvrs_helper.bvrs_has_highlight:
            raise Exception("Picker with selection must also have highlight")
        if not bvrs_helper.bvrs_has_highlight:
            raise Exception("Picker requires highlight")
        return bvrs_helper

    def _add_lines(self):
        context = {
            **self.bvrs_helper.bvrs_context(),
            "update_url": self.widget_spec.values.get("updateUrl"),
            "item_name": self.ilh.working_item_name,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_helper.bvrs_default_props())

    def _add_packages(self):
        self.output.set_flags(["utils/ValuePicker"])

    def get_spec_extension(self, places):
        extension = {}
        if not self.ilh.maybe_add_items_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no items pipeline")
        return extension
