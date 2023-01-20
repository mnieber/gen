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
from titan.react_view_pkg.pkg.builders.icon_builder import IconBuilder
from titan.react_view_pkg.pkg.builders.image_builder import ImageBuilder
from titan.react_view_pkg.pkg.builders.item_fields_builder import (
    ItemFieldBuilder,
    ItemFieldsBuilder,
)
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
from titan.react_view_pkg.pkg.builders.tabs_builder.tabs_builder import TabsBuilder
from titan.react_view_pkg.pkg.builders.text_builder import TextBuilder


def get_builders(widget_spec):
    result = []

    if widget_spec.is_component_def:
        result.append(ComponentDefBuilder(widget_spec))

    if not widget_spec.widget_base_types and widget_spec.is_component:
        # This builder is used if the parent builder uses an instance
        # of a component.
        result.append(ComponentBuilder(widget_spec))

    for widget_base_type in widget_spec.widget_base_types:
        builder = None

        if widget_base_type == "Array":
            builder = ArrayBuilder(widget_spec)

        elif widget_base_type == "Bar":
            builder = BarBuilder(widget_spec)

        elif widget_base_type == "Button":
            builder = ButtonBuilder(widget_spec)

        elif widget_base_type == "Card":
            builder = CardBuilder(widget_spec)

        elif widget_base_type == "ColSkewer":
            builder = ColSkewerBuilder(widget_spec)

        elif widget_base_type == "Children":
            builder = ChildrenBuilder(widget_spec)

        if widget_base_type == "Const":
            builder = ConstBuilder(widget_spec)

        elif widget_base_type == "Div":
            builder = DivBuilder(widget_spec)

        elif widget_base_type == "Empty":
            builder = EmptyBuilder(widget_spec)

        elif widget_base_type == "FormField":
            builder = FormFieldBuilder(widget_spec)

        elif widget_base_type == "FormFields":
            builder = FormFieldsBuilder(widget_spec)

        elif widget_base_type == "FormStateProvider":
            builder = FormStateProviderBuilder(widget_spec)

        elif widget_base_type == "Icon":
            builder = IconBuilder(widget_spec)

        elif widget_base_type == "ItemField":
            builder = ItemFieldBuilder(widget_spec)

        elif widget_base_type == "ItemFields":
            builder = ItemFieldsBuilder(widget_spec)

        elif widget_base_type == "Layout":
            builder = LayoutBuilder(widget_spec)

        elif widget_base_type == "ListView":
            builder = ListViewBuilder(widget_spec)

        elif widget_base_type == "ListViewItem":
            builder = ListViewItemBuilder(widget_spec)

        elif widget_base_type == "LviButtons":
            builder = LviButtonsBuilder(widget_spec)

        elif widget_base_type == "Image":
            builder = ImageBuilder(widget_spec)

        elif widget_base_type == "Picker":
            builder = PickerBuilder(widget_spec)

        elif widget_base_type == "Spinner":
            builder = SpinnerBuilder(widget_spec)

        elif widget_base_type == "StateProvider":
            builder = StateProviderBuilder(widget_spec)

        elif widget_base_type == "Stepper":
            builder = StepperBuilder(widget_spec)

        elif widget_base_type == "Tabs":
            builder = TabsBuilder(widget_spec)

        elif widget_base_type == "Text":
            builder = TextBuilder(widget_spec)

        elif widget_base_type == "RowSkewer":
            builder = RowSkewerBuilder(widget_spec)

        if builder:
            result.append(builder)
        else:
            raise Exception(f"Unknown widget base type: {widget_base_type}")

    return result
