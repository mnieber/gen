from titan.react_view_pkg.pkg.builders.array_builder import ArrayBuilder
from titan.react_view_pkg.pkg.builders.bar_builder import BarBuilder
from titan.react_view_pkg.pkg.builders.button_builder import ButtonBuilder
from titan.react_view_pkg.pkg.builders.card_builder import CardBuilder
from titan.react_view_pkg.pkg.builders.children_builder import ChildrenBuilder
from titan.react_view_pkg.pkg.builders.component_builder import ComponentBuilder
from titan.react_view_pkg.pkg.builders.div_builder import DivBuilder
from titan.react_view_pkg.pkg.builders.empty_builder import EmptyBuilder
from titan.react_view_pkg.pkg.builders.item_fields_builder import (
    ItemFieldBuilder,
    ItemFieldsBuilder,
)
from titan.react_view_pkg.pkg.builders.layout_builder import LayoutBuilder
from titan.react_view_pkg.pkg.builders.list_view_builder import ListViewBuilder
from titan.react_view_pkg.pkg.builders.list_view_item_builder import ListViewItemBuilder
from titan.react_view_pkg.pkg.builders.lvi_buttons_builder import LviButtonsBuilder
from titan.react_view_pkg.pkg.builders.picker_builder import PickerBuilder
from titan.react_view_pkg.pkg.builders.spinner_builder import SpinnerBuilder
from titan.react_view_pkg.pkg.builders.text_builder import TextBuilder


def get_builders(widget_spec):
    result = []
    if not widget_spec.widget_base_types and widget_spec.is_component:
        # This builder is used if the parent builder uses an instance
        # of a component.
        result.append(ComponentBuilder(widget_spec))

    for widget_base_type in widget_spec.widget_base_types:
        builder = None

        if widget_base_type == "Layout":
            builder = LayoutBuilder(widget_spec)

        elif widget_base_type == "Card":
            builder = CardBuilder(widget_spec)

        elif widget_base_type == "Text":
            builder = TextBuilder(widget_spec)

        elif widget_base_type == "Bar":
            builder = BarBuilder(widget_spec)

        elif widget_base_type == "Div":
            builder = DivBuilder(widget_spec)

        elif widget_base_type == "Empty":
            builder = EmptyBuilder(widget_spec)

        elif widget_base_type == "Children":
            builder = ChildrenBuilder(widget_spec)

        elif widget_base_type == "Array":
            builder = ArrayBuilder(widget_spec)

        elif widget_base_type == "Spinner":
            builder = SpinnerBuilder(widget_spec)

        elif widget_base_type == "Picker":
            builder = PickerBuilder(widget_spec)

        elif widget_base_type == "Button":
            builder = ButtonBuilder(widget_spec)

        elif widget_base_type == "ItemFields":
            builder = ItemFieldsBuilder(widget_spec)

        elif widget_base_type == "ItemField":
            builder = ItemFieldBuilder(widget_spec)

        elif widget_base_type == "ListView":
            builder = ListViewBuilder(widget_spec)

        elif widget_base_type == "ListViewItem":
            builder = ListViewItemBuilder(widget_spec)

        elif widget_base_type == "LviButtons":
            builder = LviButtonsBuilder(widget_spec)

        elif widget_base_type == "StateProvider":
            builder = DivBuilder(widget_spec)

        if builder:
            result.append(builder)
        else:
            raise Exception(f"Unknown widget base type: {widget_base_type}")

    return result
