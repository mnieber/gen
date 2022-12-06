from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder

from .picker_builder_tpl import picker_div_tpl, picker_handler_tpl, picker_imports_tpl


class PickerBuilder(Builder):
    def __post_init__(self):
        self.item_name = self.named_item_list_term.data
        self.items_name = plural(self.item_name)

    def build(self):
        self._add_packages()
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = {"item": self.item_name}

        # Add preamble
        handler_code = self.render_str(
            picker_handler_tpl, context, "picker_builder_handler.j2"
        )
        self.add_preamble_lines([handler_code])

        # Add imports
        self.add_import_lines([picker_imports_tpl])

        # Add div
        div = self.render_str(picker_div_tpl, context, "picker_builder_div.j2")
        self.add_lines([div])

    def _add_default_props(self):
        append_uniq(self.output.default_props, f"{self.items_name}:selection")
        append_uniq(self.output.default_props, f"{self.items_name}:highlight")

    def _add_packages(self):
        packages = self.output.react_packages_by_module_name.setdefault("utils", [])
        extend_uniq(packages, ["ValuePicker"])
