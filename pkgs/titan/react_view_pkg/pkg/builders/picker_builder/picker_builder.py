from pathlib import Path

from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper

from moonleap import get_tpl
from moonleap.utils.fp import extend_uniq


class PickerBuilder(Builder):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        self.bvrs_helper = BvrsHelper(widget_spec, self.ilh.array_item_name)
        if (
            self.bvrs_helper.bvrs_has_selection
            and not self.bvrs_helper.bvrs_has_highlight
        ):
            raise Exception("Picker with selection must also have highlight")
        if not self.bvrs_helper.bvrs_has_highlight:
            raise Exception("Picker requires highlight")

    def build(self):
        self._add_packages()
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = {
            **self.bvrs_helper.bvrs_context(),
            "update_url": self.widget_spec.values.get("updateUrl"),
            "item_name": self.ilh.array_item_name,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_helper.bvrs_default_props())

    def _add_packages(self):
        self.output.set_flags(["utils/ValuePicker"])

    def update_widget_spec(self):
        self.ilh.update_widget_spec()
