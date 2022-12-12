from moonleap.utils.fp import extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .tpl import tpls


class PickerBuilder(BvrsBuilderMixin, Builder):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)
        if self.bvrs_has_selection and not self.bvrs_has_highlight:
            raise Exception("Picker with selection must also have highlight")
        if not self.bvrs_has_highlight:
            raise Exception("Picker requires highlight")

    def build(self):
        self._add_packages()
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = {
            "__": {
                **self.bvrs_context(),
                "update_url": self.widget_spec.get_value_by_name("updateUrl"),
                "item": self.bvrs_item_name,
            },
        }

        self.add(
            preamble_lines=[tpls.render("picker_handler_tpl", context)],
            lines=[tpls.render("picker_div_tpl", context)],
            imports_lines=[tpls.render("picker_imports_tpl", context)],
            props_lines=[tpls.render("picker_props_tpl", context)],
        )

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _add_packages(self):
        packages = self.output.react_packages_by_module_name.setdefault("utils", [])
        extend_uniq(packages, ["ValuePicker"])
