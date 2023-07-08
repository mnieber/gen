from titan.react_view_pkg.pkg.builders.children_builder import ChildrenBuilder
from titan.react_view_pkg.pkg.builders.component_builder import ComponentBuilder
from titan.react_view_pkg.pkg.builders.component_def_builder import ComponentDefBuilder
from titan.react_view_pkg.pkg.builders.div_builder import DivBuilder
from titan.react_view_pkg.pkg.builders.empty_builder import EmptyBuilder
from titan.react_view_pkg.pkg.builders.form_state_provider_builder.form_state_provider_builder import (
    FormStateProviderBuilder,
)
from titan.react_view_pkg.pkg.builders.generic_builder import GenericBuilder
from titan.react_view_pkg.pkg.builders.key_handler_builder import KeyHandlerBuilder
from titan.react_view_pkg.pkg.builders.list_view_builder.list_view_builder import (
    ListViewBuilder,
)
from titan.react_view_pkg.pkg.builders.list_view_item_builder.list_view_item_builder import (
    ListViewItemBuilder,
)
from titan.react_view_pkg.pkg.builders.lvi_buttons_builder.lvi_buttons_builder import (
    LviButtonsBuilder,
)
from titan.react_view_pkg.pkg.builders.markdown_builder import MarkdownBuilder
from titan.react_view_pkg.pkg.builders.picker_builder.picker_builder import (
    PickerBuilder,
)
from titan.react_view_pkg.pkg.builders.resize_detector_builder import (
    ResizeDetectorBuilder,
)
from titan.react_view_pkg.pkg.builders.spinner_builder.spinner_builder import (
    SpinnerBuilder,
)
from titan.react_view_pkg.pkg.builders.state_provider_builder.state_provider_builder import (
    StateProviderBuilder,
)
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

        if widget_base_type in ChildrenBuilder.type:
            builder = ChildrenBuilder(widget_spec)

        elif widget_base_type == DivBuilder.type:
            builder = DivBuilder(widget_spec)

        elif widget_base_type == EmptyBuilder.type:
            builder = EmptyBuilder(widget_spec)

        elif widget_base_type == FormStateProviderBuilder.type:
            builder = FormStateProviderBuilder(widget_spec)

        elif widget_base_type == KeyHandlerBuilder.type:
            builder = KeyHandlerBuilder(widget_spec)

        elif widget_base_type == ListViewBuilder.type:
            builder = ListViewBuilder(widget_spec)

        elif widget_base_type == ListViewItemBuilder.type:
            builder = ListViewItemBuilder(widget_spec)

        elif widget_base_type == LviButtonsBuilder.type:
            builder = LviButtonsBuilder(widget_spec)

        elif widget_base_type == MarkdownBuilder.type:
            builder = MarkdownBuilder(widget_spec)

        elif widget_base_type == PickerBuilder.type:
            builder = PickerBuilder(widget_spec)

        elif widget_base_type == ResizeDetectorBuilder.type:
            builder = ResizeDetectorBuilder(widget_spec)

        elif widget_base_type == SpinnerBuilder.type:
            builder = SpinnerBuilder(widget_spec)

        elif widget_base_type == StateProviderBuilder.type:
            builder = StateProviderBuilder(widget_spec)

        elif widget_base_type == TextBuilder.type:
            builder = TextBuilder(widget_spec)

        if builder:
            result.append(builder)
        else:
            raise Exception(f"Unknown widget base type: {widget_base_type}")

    return result
