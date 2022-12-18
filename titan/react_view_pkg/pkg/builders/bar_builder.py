from moonleap.utils.quote import quote_all
from titan.react_view_pkg.pkg.builder import Builder


class BarBuilder(Builder):
    def __post_init__(self):
        self._widgets = []
        self._has_widgets = False
        self.lhs_slot = None
        self.lhs_wrapper = None
        self.middle_slot = None
        self.rhs_slot = None
        self.rhs_wrapper = None

    def _get_widgets(self):
        if self._has_widgets:
            return
        self._has_widgets = True

        if lhs_slot := self.widget_spec.get_place("LhsSlot"):
            self.lhs_slot = lhs_slot
            self._widgets.append(lhs_slot)

        if lhs_contents := self.widget_spec.get_place("LhsContents"):
            self.lhs_wrapper = self.widget_spec.get_place("LhsWrapper")
            assert self.lhs_wrapper
            self.lhs_wrapper.child_widget_specs.append(lhs_contents)
            self._widgets.append(self.lhs_wrapper)

        if middle_slot := self.widget_spec.get_place("MiddleSlot"):
            self.middle_slot = middle_slot
            self._widgets.append(middle_slot)

        if rhs_slot := self.widget_spec.get_place("RhsSlot"):
            self.rhs_slot = rhs_slot
            self._widgets.append(rhs_slot)

        if rhs_contents := self.widget_spec.get_place("RhsContents"):
            self.rhs_wrapper = self.widget_spec.get_place("RhsWrapper")
            assert self.rhs_wrapper
            self.rhs_wrapper.child_widget_specs.append(rhs_contents)
            self._widgets.append(self.rhs_wrapper)

        if not self._widgets:
            raise Exception("Bar must have at least one used slot")

    def get_spec_extension(self, places):
        result = {}

        if "LhsWrapper" not in places:
            cn = self.widget_spec.values.get("cnLhs") or "Lhs"
            result[f"LhsWrapper with Div, RowSkewer[cn={cn}.justify-start]"] = "pass"

        if "RhsWrapper" not in places:
            cn = self.widget_spec.values.get("cnRhs") or "Lhs"
            result[f"RhsWrapper with Div, RowSkewer[cn={cn}.justify-end]"] = "pass"

        return result

    def patch_widget_spec(self):
        self._get_widgets()
        styles = []

        if self.lhs_slot or self.lhs_wrapper:
            styles += ["1fr"]

        if self.middle_slot:
            styles += ["0fr"]

        if self.rhs_slot or self.rhs_wrapper:
            styles += ["0fr"] if (self.lhs_slot and not self.middle_slot) else ["1fr"]

        self.widget_spec.div.prepend_styles(
            quote_all(["grid", f'grid-cols-[{",".join(styles)}]'])
        )

    def build(self):
        with self.widget_spec.memo():
            self.patch_widget_spec()
            self._get_widgets()

            if self.lhs_wrapper or self.rhs_wrapper:
                self.add(imports=["import { rowSkewer } from 'src/frames/components';"])
            self._add_div_open()
            self._add_child_widgets(self._widgets)
            self._add_div_close()
