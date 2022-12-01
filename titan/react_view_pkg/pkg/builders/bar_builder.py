from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.div_attrs import update_div_attrs


class BarBuilder(Builder):
    def build(self, div_attrs=None):
        left_slot = self.widget_spec.find_child_with_place("LeftSlot")
        middle_slot = self.widget_spec.find_child_with_place("MiddleSlot")
        right_slot = self.widget_spec.find_child_with_place("RightSlot")

        widgets = []
        styles = []

        if left_slot:
            widgets.append(left_slot)
            styles += ["1fr"]

        if middle_slot:
            widgets.append(middle_slot)
            styles += ["0fr"]

        if right_slot:
            widgets.append(right_slot)
            styles += ["0fr"] if (left_slot and not middle_slot) else ["1fr"]
            right_slot.styles = [
                '"flex flex-row justify-end items-center"'
            ] + right_slot.styles

        self._add_div_open(
            update_div_attrs(
                div_attrs, prefix_classes=[f'"grid grid-cols-[{",".join(styles)}]"']
            )
        )
        self._add_child_widgets(child_widget_specs=widgets)
        self._add_div_close()
