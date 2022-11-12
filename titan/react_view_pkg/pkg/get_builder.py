from titan.react_view_pkg.pkg.builder import Builder


def get_builder(widget_spec, parent_builder, level) -> Builder:
    from titan.react_view_pkg.pkg.bar_builder import BarBuilder
    from titan.react_view_pkg.pkg.card_builder import CardBuilder
    from titan.react_view_pkg.pkg.children_builder import ChildrenBuilder
    from titan.react_view_pkg.pkg.component_builder import ComponentBuilder
    from titan.react_view_pkg.pkg.div_builder import DivBuilder
    from titan.react_view_pkg.pkg.layout_builder import LayoutBuilder

    if widget_spec.is_component and level > 0:
        return ComponentBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Layout":
        return LayoutBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Card":
        return CardBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Bar":
        return BarBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Div":
        return DivBuilder(widget_spec, parent_builder, level)

    if widget_spec.widget_base_type == "Children":
        return ChildrenBuilder(widget_spec, parent_builder, level)

    raise Exception(f"Unknown widget base type: {widget_spec.widget_base_type}")
