from titan.react_view_pkg.pkg.builder import Builder


class BarBuilder(Builder):
    type = "Bar"

    def __post_init__(self):
        self._widgets = []
        self.left_slot = None
        self.lhs_wrapper = None
        self.middle_slot = None
        self.right_slot = None
        self.rhs_wrapper = None

    def _update_widgets(self):
        self._widgets = []

        if left_slot := self.widget_spec.get_place("LeftSlot"):
            self.left_slot = left_slot
            self._widgets.append(left_slot)

        if lhs_wrapper := self.widget_spec.get_place("LhsWrapper"):
            self.lhs_wrapper = lhs_wrapper
            self._widgets.append(lhs_wrapper)

        if middle_slot := self.widget_spec.get_place("MiddleSlot"):
            self.middle_slot = middle_slot
            self._widgets.append(middle_slot)

        if right_slot := self.widget_spec.get_place("RightSlot"):
            self.right_slot = right_slot
            self._widgets.append(right_slot)

        if rhs_wrapper := self.widget_spec.get_place("RhsWrapper"):
            self.rhs_wrapper = rhs_wrapper
            self._widgets.append(rhs_wrapper)

    def get_spec_extension(self, places):
        result = {}

        if (
            "LeftSlot" not in places
            and "LhsWrapper" not in places
            and "LhsContents" in places
        ):
            cn = self.get_value("cnLhs") or "Lhs"
            result[f"LhsWrapper with Div, RowSkewer[cn={cn},justify-start]"] = "pass"

        if (
            "RightSlot" not in places
            and "RhsWrapper" not in places
            and "RhsContents" in places
        ):
            cn = self.get_value("cnRhs") or "Rhs"
            result[f"RhsWrapper with Div, RowSkewer[cn={cn},justify-end]"] = "pass"

        return result

    def update_widget_spec(self):
        self._update_widgets()
        styles = []

        if self.lhs_wrapper:
            if lhs_contents := self.widget_spec.get_place("LhsContents"):
                self.lhs_wrapper.add_child_widget_spec(lhs_contents)
                self.widget_spec.remove_child_widget_spec(lhs_contents)

        if self.rhs_wrapper:
            if rhs_contents := self.widget_spec.get_place("RhsContents"):
                self.rhs_wrapper.add_child_widget_spec(rhs_contents)
                self.widget_spec.remove_child_widget_spec(rhs_contents)

        if self.left_slot or self.lhs_wrapper:
            styles += ["1fr"]

        if self.middle_slot:
            styles += ["0fr"]

        if self.right_slot or self.rhs_wrapper:
            styles += ["0fr"] if (self.left_slot and not self.middle_slot) else ["1fr"]

        self.widget_spec.div.prepend_styles(["grid", f'grid-cols-[{",".join(styles)}]'])

    def build(self):
        self._update_widgets()
        if not self._widgets:
            raise Exception("Bar must have at least one used slot")

        self.output.add(imports=["import { rowSkewer } from 'src/frames/components';"])
        if not self.widget_spec.is_component_def:
            self.output.add(lines=["<></>{/* Bar */}<></>"])
        self._add_div_open()
        self._add_child_widgets(self._widgets)
        self._add_div_close()
