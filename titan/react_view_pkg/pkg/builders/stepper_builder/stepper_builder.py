from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.widgets_pkg.pkg.load_widget_specs.create_widget_spec import \
    create_widget_spec


class StepperBuilder(Builder):
    def build(self):
        self.use_uniform_height = self.widget_spec.values.get("uniformHeight")
        self.item_name = self.ilh.array_item_name
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(self._get_child_widget_output())
        context = {
            "__const_name": const_name,
            "__items_expr": self.ilh.item_list_data_path(),
            "__item_name": self.item_name,
            "__child_widget_div": child_widget_div,
            "__uniform_height": self.use_uniform_height,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def get_spec_extension(self, places):
        if "Child" not in places:
            src_dict = self.widget_spec.src_dict
            lhs_dict, middle_dict, rhs_dict = None, None, None
            for k, v in src_dict.items():
                ws, _ = create_widget_spec(k, v, None)
                if ws.place == "LhsContents":
                    lhs_dict = {k: v}
                if ws.place == "MiddleSlot":
                    middle_dict = {k: v}
                if ws.place == "RhsContents":
                    rhs_dict = {k: v}

            lhs_dict = lhs_dict or {
                "LhsContents with backButton as Const": {
                    "Child with Div, Button[onClick=moveBack.cn=__Back]": {
                        "Text": "value=Back"
                    }
                }
            }
            middle_dict = middle_dict or {"MiddleSlot with Empty": "pass"}
            rhs_dict = rhs_dict or {
                "RhsContents with forwardButton as Const": {
                    "Child with Div, Button[onClick=moveForward.cn=__Forward]": {
                        "Text": "value=Forward"
                    }
                }
            }
            return {
                "Child with Bar[cn=__Stepper]": {**lhs_dict, **middle_dict, **rhs_dict}
            }

    def _get_const_name(self):
        assert self.item_name
        return self.item_name + ("Divs" if self.use_uniform_height else "Div")

    def update_widget_spec(self):
        self.ilh.update_widget_spec()
        tpl = get_tpl(Path(__file__).parent / "tpl_div.tsx.j2", {})
        self.widget_spec.root.div.append_attrs([tpl.get_section("attrs")])

    def _get_child_widget_output(self):
        from titan.react_view_pkg.pkg.build import build

        child_widget_spec = self.widget_spec.get_place("Child")
        assert child_widget_spec

        with child_widget_spec.memo():
            child_widget_spec.div.key = f"{self.item_name}.id"
            if self.use_uniform_height:
                child_widget_spec.div.append_styles(
                    [f"idx === {self.item_name}Idx ? 'visible' : 'invisible'"]
                )
            return build(child_widget_spec)
