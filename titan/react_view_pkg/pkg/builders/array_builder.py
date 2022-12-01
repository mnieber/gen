import ramda as R

from moonleap.parser.term import Term, word_to_term
from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

template_str = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item }}: {{ item|u0 }}T) => {
  {{ child_widget_div }}
});
"""
)


class ArrayBuilder(Builder):
    @property
    def named_items_term(self):
        items_str = self.widget_spec.values["items"]
        result = word_to_term(items_str)
        assert result
        return result

    @property
    def item_list(self):
        named_items_term = self.named_items_term
        items_term = Term(data=named_items_term.data, tag=named_items_term.tag)
        item_list = R.head(
            x.item_list
            for x in get_type_reg().items
            if x.item_list.meta.term.as_normalized_str == items_term.as_normalized_str
        )
        return item_list

    def build(self, classes=None, handlers=None):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        named_items_term = self.named_items_term
        child_widget_spec = self.widget_spec.find_child_with_place("Child")
        child_builder = get_builder(child_widget_spec, self, self.level + 1)
        child_builder.build()
        child_widget_div = child_builder.output.div

        root_component = self.root_builder.widget_spec.component

        pipeline, item_list_expr = root_component.get_pipeline_and_expr(
            term=named_items_term
        )
        if not pipeline:
            raise Exception(f"Could not find pipeline for: {named_items_term}")

        t = get_template_from_str(template_str)
        const_name = self.widget_spec.widget_name
        code = t.render(
            {
                "const_name": const_name,
                "items_expr": item_list_expr,
                "item": self.item_list.item.item_name,
                "child_widget_div": child_widget_div,
            }
        )
        self.output.preamble_lines.extend([code])
        self.add_lines(["{%s}" % const_name])
