from titan.react_view_pkg.pkg.builder import Builder


class BarBuilder(Builder):
    def __post_init__(self):
        self._widgets = []
        self._has_widgets = False
        self.lhs_slot = None
        self.middle_slot = None
        self.rhs_slot = None

    def _get_widgets(self):
        if self._has_widgets:
            return
        self._has_widgets = True

        if lhs_slot := self.widget_spec.find_child_with_place("LhsSlot"):
            self.lhs_slot = lhs_slot
            self._widgets.append(lhs_slot)

        if middle_slot := self.widget_spec.find_child_with_place("MiddleSlot"):
            self.middle_slot = middle_slot
            self._widgets.append(middle_slot)

        if rhs_slot := self.widget_spec.find_child_with_place("RhsSlot"):
            self.rhs_slot = rhs_slot
            self._widgets.append(rhs_slot)

        if not self._widgets:
            raise Exception("Bar must have at least one used slot")

    def patch_widget_spec(self):
        self._get_widgets()
        styles = []

        if self.lhs_slot:
            styles += ["1fr"]

        if self.middle_slot:
            styles += ["0fr"]

        if self.rhs_slot:
            styles += ["0fr"] if (self.lhs_slot and not self.middle_slot) else ["1fr"]

        self.widget_spec.div.prepend_styles([f'"grid grid-cols-[{",".join(styles)}]"'])

    def build(self):
        self.patch_widget_spec()
        self._get_widgets()

        self.add(imports=["import { rowSkewer } from 'src/frames/components';"])
        self._add_div_open()
        self._add_child_widgets(self._widgets)
        self._add_div_close()
