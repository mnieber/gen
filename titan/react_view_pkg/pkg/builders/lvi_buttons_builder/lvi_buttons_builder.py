from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper


class LviButtonsBuilder(Builder):
    def __post_init__(self):
        self.bvrs_helper = BvrsHelper(self.widget_spec, self.ilh.array_item_name)

    def build(self):
        context = self._get_context()
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_context(self):
        return {
            **self.bvrs_helper.bvrs_context(),
            "item_name": self.ih.array_item_name,
            "component_name": self.widget_spec.widget_class_name,
            "uikit": self.use_uikit,
        }
