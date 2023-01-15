from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class SpinnerBuilder(Builder):
    def build(self):
        item_list_data_path = self.ilh.item_list_data_path()
        item_data_path = self.ih.item_data_path()

        context = {
            "test": (
                f"!{item_list_data_path}?.length"
                if item_list_data_path
                else f"!{item_data_path}"
            ),
            "data_path": item_list_data_path or item_data_path,
            "guard": self.widget_spec.values.get("guard"),
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)
