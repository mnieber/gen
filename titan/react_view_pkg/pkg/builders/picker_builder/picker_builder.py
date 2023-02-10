from pathlib import Path

from moonleap import get_tpl
from moonleap.utils.fp import extend_uniq
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper


class PickerBuilder(Builder):
    type = "Picker"

    def __post_init__(self):
        self.save = self.get_value("save")

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
        form_data = self.widget_spec.get_form_data(recurse=True)
        context = dict(
            **self.bvrs_helper.bvrs_context(),
            update_url=self.widget_spec.values.get("updateUrl"),
            item_name=self.ilh.working_item_name,
            mutation=form_data.mutation,
            editing_bvr=form_data.editing_bvr,
            path_to_items=self.ilh.item_list_data_path(),
            save=self.save,
            spinner=self.get_value("spinner"),
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_helper.bvrs_default_props())

    def _add_packages(self):
        self.output.set_flags(["utils/ValuePicker"])

    def get_spec_extension(self, places):
        extension = {}
        if not self.ilh.maybe_add_items_pipeline_to_spec_extension(extension):
            raise Exception("PickerBuilder: no 'items' pipeline")

        if self.save:
            if not self.ih.maybe_add_save_pipeline_to_spec_extension(extension):
                raise Exception("PickerBuilder: no 'save' pipeline")

        return extension
