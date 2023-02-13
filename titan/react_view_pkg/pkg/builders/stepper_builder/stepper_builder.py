from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.widgetspec.get_place_dict import get_place_dict


class StepperBuilder(Builder):
    type = "Stepper"

    def build(self):
        self.use_uniform_height = self.widget_spec.get_value("uniformHeight")
        self.item_name = self.ilh.working_item_name
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(self._get_child_widget_output())
        context = {
            "__child_widget_div": child_widget_div,
            "__const_name": const_name,
            "__guard": self.widget_spec.get_value("guard"),
            "__item_name": self.item_name,
            "__items_expr": self.ilh.item_list_data_path(),
            "__uniform_height": self.use_uniform_height,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def get_spec_extension(self, places):
        if "Child" not in places:
            src_dict = self.widget_spec.src_dict
            lhs_dict = get_place_dict(src_dict, "LhsContents") or {
                "LhsContents with backButton as Const": {
                    "Child with Div, Button": {
                        "__onClick__": "moveBack",
                        "__class__": "__Back",
                        "Text": {"text": "Back"},
                    }
                }
            }
            middle_dict = get_place_dict(src_dict, "MiddleSlot") or {
                "MiddleSlot with Empty": "pass"
            }
            rhs_dict = get_place_dict(src_dict, "RhsContents") or {
                "RhsContents with forwardButton as Const": {
                    "Child with Div, Button": {
                        "__onClick__": "moveForward",
                        "__class__": "__Forward",
                        "Text": {"__text__": "Forward"},
                    }
                }
            }
            return {
                "Child with Bar": {
                    "__class__": "__Stepper",
                    **lhs_dict,
                    **middle_dict,
                    **rhs_dict,
                }
            }

    def _get_const_name(self):
        assert self.item_name
        return self.item_name + ("Divs" if self.use_uniform_height else "Div")

    def get_spec_extension(self, places):
        extension = {}
        if not self.ilh.maybe_add_items_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no items pipeline")
        return extension

    def update_widget_spec(self):
        tpl = get_tpl(Path(__file__).parent / "tpl_div.tsx.j2", {})
        self.widget_spec.root.div.append_attrs([tpl.get_section("attrs")])

    def _get_child_widget_output(self):
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        child_widget_spec = self.widget_spec.get_place("Child")
        assert child_widget_spec

        with child_widget_spec.memo(["div"]):
            child_widget_spec.div.key = f"{self.item_name}.id"
            if self.use_uniform_height:
                child_widget_spec.div.append_styles(
                    [f"idx === {self.item_name}Idx ? 'visible' : 'invisible'"]
                )
            return build_widget_spec(child_widget_spec)
