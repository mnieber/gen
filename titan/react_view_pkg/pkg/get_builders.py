from titan.react_view_pkg.pkg.builders.array_builder.array_builder import ArrayBuilder
from titan.react_view_pkg.pkg.builders.bar_builder import BarBuilder
from titan.react_view_pkg.pkg.builders.button_builder import ButtonBuilder
from titan.react_view_pkg.pkg.builders.card_builder import CardBuilder
from titan.react_view_pkg.pkg.builders.children_builder import ChildrenBuilder
from titan.react_view_pkg.pkg.builders.col_skewer_builder import ColSkewerBuilder
from titan.react_view_pkg.pkg.builders.component_builder import ComponentBuilder
from titan.react_view_pkg.pkg.builders.component_def_builder import ComponentDefBuilder
from titan.react_view_pkg.pkg.builders.const_builder.const_builder import ConstBuilder
from titan.react_view_pkg.pkg.builders.div_builder import DivBuilder
from titan.react_view_pkg.pkg.builders.empty_builder import EmptyBuilder
from titan.react_view_pkg.pkg.builders.form_field_builder import FormFieldBuilder
from titan.react_view_pkg.pkg.builders.form_fields_builder import FormFieldsBuilder
from titan.react_view_pkg.pkg.builders.form_state_provider_builder.form_state_provider_builder import (
    FormStateProviderBuilder,
)
from titan.react_view_pkg.pkg.builders.generic_builder import GenericBuilder
from titan.react_view_pkg.pkg.builders.icon_builder import IconBuilder
from titan.react_view_pkg.pkg.builders.image_builder import ImageBuilder
from titan.react_view_pkg.pkg.builders.item_fields_builder import (
    ItemFieldBuilder,
    ItemFieldsBuilder,
)
from titan.react_view_pkg.pkg.builders.key_handler_builder import KeyHandlerBuilder
from titan.react_view_pkg.pkg.builders.layout_builder import LayoutBuilder
from titan.react_view_pkg.pkg.builders.list_view_builder.list_view_builder import (
    ListViewBuilder,
)
from titan.react_view_pkg.pkg.builders.list_view_item_builder.list_view_item_builder import (
    ListViewItemBuilder,
)
from titan.react_view_pkg.pkg.builders.lvi_buttons_builder.lvi_buttons_builder import (
    LviButtonsBuilder,
)
from titan.react_view_pkg.pkg.builders.picker_builder.picker_builder import (
    PickerBuilder,
)
from titan.react_view_pkg.pkg.builders.resize_detector_builder import (
    ResizeDetectorBuilder,
)
from titan.react_view_pkg.pkg.builders.row_skewer_builder import RowSkewerBuilder
from titan.react_view_pkg.pkg.builders.spinner_builder.spinner_builder import (
    SpinnerBuilder,
)
from titan.react_view_pkg.pkg.builders.state_provider_builder.state_provider_builder import (
    StateProviderBuilder,
)
from titan.react_view_pkg.pkg.builders.stepper_builder.stepper_builder import (
    StepperBuilder,
)
from titan.react_view_pkg.pkg.builders.switch_builder import SwitchBuilder
from titan.react_view_pkg.pkg.builders.tabs_builder.tabs_builder import TabsBuilder
from titan.react_view_pkg.pkg.builders.text_builder import TextBuilder


def get_builders(widget_spec):
    result = [GenericBuilder(widget_spec)]

    if widget_spec.is_component_def:
        result.append(ComponentDefBuilder(widget_spec))

    if not widget_spec.widget_base_types and widget_spec.is_component:
        # This builder is used if the parent builder uses an instance
        # of a component.
        result.append(ComponentBuilder(widget_spec))

    for widget_base_type in widget_spec.widget_base_types:
        builder = None

        if widget_base_type == ArrayBuilder.type:
            builder = ArrayBuilder(widget_spec)

        elif widget_base_type == BarBuilder.type:
            builder = BarBuilder(widget_spec)

        elif widget_base_type == ButtonBuilder.type:
            builder = ButtonBuilder(widget_spec)

        elif widget_base_type == CardBuilder.type:
            builder = CardBuilder(widget_spec)

        elif widget_base_type == ColSkewerBuilder.type:
            builder = ColSkewerBuilder(widget_spec)

        elif widget_base_type in ChildrenBuilder.type:
            builder = ChildrenBuilder(widget_spec)

        if widget_base_type == ConstBuilder.type:
            builder = ConstBuilder(widget_spec)

        elif widget_base_type == DivBuilder.type:
            builder = DivBuilder(widget_spec)

        elif widget_base_type == EmptyBuilder.type:
            builder = EmptyBuilder(widget_spec)

        elif widget_base_type == FormFieldBuilder.type:
            builder = FormFieldBuilder(widget_spec)

        elif widget_base_type == FormFieldsBuilder.type:
            builder = FormFieldsBuilder(widget_spec)

        elif widget_base_type == FormStateProviderBuilder.type:
            builder = FormStateProviderBuilder(widget_spec)

        elif widget_base_type == IconBuilder.type:
            builder = IconBuilder(widget_spec)

        elif widget_base_type == ItemFieldBuilder.type:
            builder = ItemFieldBuilder(widget_spec)

        elif widget_base_type == ItemFieldsBuilder.type:
            builder = ItemFieldsBuilder(widget_spec)

        elif widget_base_type == KeyHandlerBuilder.type:
            builder = KeyHandlerBuilder(widget_spec)

        elif widget_base_type == LayoutBuilder.type:
            builder = LayoutBuilder(widget_spec)

        elif widget_base_type == ListViewBuilder.type:
            builder = ListViewBuilder(widget_spec)

        elif widget_base_type == ListViewItemBuilder.type:
            builder = ListViewItemBuilder(widget_spec)

        elif widget_base_type == LviButtonsBuilder.type:
            builder = LviButtonsBuilder(widget_spec)

        elif widget_base_type == ImageBuilder.type:
            builder = ImageBuilder(widget_spec)

        elif widget_base_type == PickerBuilder.type:
            builder = PickerBuilder(widget_spec)

        elif widget_base_type == ResizeDetectorBuilder.type:
            builder = ResizeDetectorBuilder(widget_spec)

        elif widget_base_type == SpinnerBuilder.type:
            builder = SpinnerBuilder(widget_spec)

        elif widget_base_type == StateProviderBuilder.type:
            builder = StateProviderBuilder(widget_spec)

        elif widget_base_type == StepperBuilder.type:
            builder = StepperBuilder(widget_spec)

        elif widget_base_type == SwitchBuilder.type:
            builder = SwitchBuilder(widget_spec)

        elif widget_base_type == TabsBuilder.type:
            builder = TabsBuilder(widget_spec)

        elif widget_base_type == TextBuilder.type:
            builder = TextBuilder(widget_spec)

        elif widget_base_type == RowSkewerBuilder.type:
            builder = RowSkewerBuilder(widget_spec)

        if builder:
            result.append(builder)
        else:
            raise Exception(f"Unknown widget base type: {widget_base_type}")

    return result
