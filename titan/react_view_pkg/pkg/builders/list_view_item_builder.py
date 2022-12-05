from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.verbatim_builder import VerbatimBuilder


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

    def build(self):
        styles = []
        props = []

        if self.helpers.has_selection:
            styles += [
                f"{{'{self.helpers.component_name}--selected': props.isSelected",
                f"'{self.helpers.component_name}--highlighted': props.isHighlighted}}",
            ]
            props += ["{...clickHandlers(props)}"]

        if self.helpers.has_drag_and_drop:
            styles += [f"`{self.helpers.component_name}--drag-${{props.dragState}}`"]
            props += ["{...dragHandlers(props)}"]

        self.widget_spec.div_styles = styles + self.widget_spec.div_styles
        self.widget_spec.div_props = self.widget_spec.div_props + props

        inner_builder.build()
        self.output = inner_builder.output
