from titan.react_view_pkg.pkg.builder import Builder
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
from titan.react_view_pkg.pkg.builders.picker_builder import PickerBuilder
from titan.react_view_pkg.pkg.builders.spinner_builder import SpinnerBuilder
from titan.react_view_pkg.pkg.builders.text_builder import TextBuilder


def get_builder(widget_spec, parent_builder, level) -> Builder:
    if widget_spec.is_component and (level > 0 or not widget_spec.is_component_def):
        return ComponentBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Layout":
        return LayoutBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Card":
        return CardBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Text":
        return TextBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Bar":
        return BarBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Div":
        return DivBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Empty":
        return EmptyBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Children":
        return ChildrenBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Array":
        return ArrayBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Spinner":
        return SpinnerBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Picker":
        return PickerBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Button":
        return ButtonBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "ItemFields":
        return ItemFieldsBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "ItemField":
        return ItemFieldBuilder(widget_spec, parent_builder, level)

    raise Exception(f"Unknown widget base type: {widget_spec.widget_base_type}")
