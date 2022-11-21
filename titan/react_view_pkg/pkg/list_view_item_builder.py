from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.verbatim_builder import VerbatimBuilder


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
        div = self.render("components/__moonleap__/lvi_fields.tsx.j2")
        return VerbatimBuilder(*args, **kwargs, div=div)

    def _get_lvi_buttons(self, *args, **kwargs):
        div = self.render("components/__moonleap__/lvi_buttons.tsx.j2")
        return VerbatimBuilder(*args, **kwargs, div=div)

    def build(self, classes=None, handlers=None):
        inner_builder = self._get_builder(self.widget_spec, self.level)

        classes = list(classes or [])
        handlers = list(handlers or [])

        if self.helpers.has_selection:
            classes += [
                f"{{'{self.helpers.component_name}--selected': props.isSelected",
                f"'{self.helpers.component_name}--highlighted': props.isHighlighted}}",
            ]
            handlers += ["{...clickHandlers(props)}"]

        if self.helpers.has_drag_and_drop:
            classes += [f"`{self.helpers.component_name}--drag-${{props.dragState}}`"]
            handlers += ["{...dragHandlers(props)}"]

        inner_builder.build(classes, handlers)
        self.output = inner_builder.output
