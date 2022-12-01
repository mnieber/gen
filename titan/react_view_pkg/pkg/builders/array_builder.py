import ramda as R

from moonleap import kebab_to_camel
from moonleap.parser.term import Term, word_to_term
from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

template_str = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item }}: {{ item|u0 }}T) => {
  return (
    <div key={ {{ item }}.id } {{ item }}={ {{ item }} }>
      Moonleap Todo
    </div>
  );
});
"""
)


class ArrayBuilder(Builder):
    def build(self, classes=None, handlers=None):
        child_slot = self.widget_spec.find_child_with_place("Child")

        root_component = self.root_builder.widget_spec.component

        items_str = self.widget_spec.values["items"]
        named_items_term = word_to_term(items_str)

        pipeline, item_list_expr = root_component.get_pipeline_and_expr(
            term=named_items_term
        )
        if not pipeline:
            raise Exception(f"Could not find pipeline for: {items_str}")

        assert named_items_term
        items_term = Term(data=named_items_term.data, tag=named_items_term.tag)
        item_list = R.head(
            x.item_list
            for x in get_type_reg().items
            if x.item_list.meta.term.as_normalized_str == items_term.as_normalized_str
        )

        t = get_template_from_str(template_str)
        const_name = plural(self.widget_spec.component.meta.term.to_camel())
        code = t.render(
            {
                "const_name": const_name,
                "items_expr": item_list_expr,
                "item": item_list.item.item_name,
            }
        )
        self.output.preamble_lines.extend([code])
        self.add_lines(["{%s}" % const_name])
