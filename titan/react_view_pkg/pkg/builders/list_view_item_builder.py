from titan.react_view_pkg.pkg.add_child_widgets import get_child_widget_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.verbatim_builder import VerbatimBuilder
from titan.react_view_pkg.pkg.div_attrs import update_div_attrs


class ListViewItemBuilder(Builder):
    def __init__(self, widget_spec, parent_builder, level, helpers, render):
        super().__init__(widget_spec, parent_builder, level)
        self.helpers = helpers
        self.render = render
        self._register_builders()

    def _register_builders(self):
        self.register_builder_type("LviFields", self._get_lvi_fields)
        self.register_builder_type("LviButtons", self._get_lvi_buttons)

    def _get_lvi_fields(self, *args, **kwargs):
        return VerbatimBuilder(
            *args,
            **kwargs,
            div=self.render("components/__moonleap__/lvi_fields.tsx.j2"),
        )

    def _get_lvi_buttons(self, *args, **kwargs):
        return VerbatimBuilder(
            *args,
            **kwargs,
            div=self.render("components/__moonleap__/lvi_buttons.tsx.j2"),
        )

    def build(self, div_attrs=None):
        inner_builder = get_child_widget_builder(self, self.widget_spec, self.level)

        more_classes = []
        more_handlers = []

        if self.helpers.has_selection:
            more_classes += [
                f"{{'{self.helpers.component_name}--selected': props.isSelected",
                f"'{self.helpers.component_name}--highlighted': props.isHighlighted}}",
            ]
            more_handlers += ["{...clickHandlers(props)}"]

        if self.helpers.has_drag_and_drop:
            more_classes += [
                f"`{self.helpers.component_name}--drag-${{props.dragState}}`"
            ]
            more_handlers += ["{...dragHandlers(props)}"]

        inner_builder.build(
            update_div_attrs(
                div_attrs, prefix_classes=more_classes, handlers=more_handlers
            )
        )
        self.output = inner_builder.output
