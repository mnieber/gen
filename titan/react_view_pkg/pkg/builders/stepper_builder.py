from moonleap import Tpls, append_uniq, chop0
from titan.react_view_pkg.pkg.builder import Builder


class StepperBuilder(Builder):
    def build(self):
        use_uniform_height = self.widget_spec.get_value_by_name("uniformHeight")
        item_name = self.ilh.array_item_name
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(
            _get_child_widget_output(self.widget_spec, item_name, use_uniform_height)
        )
        context = {
            "__const_name": const_name,
            "__items_expr": self.ilh.item_list_data_path(),
            "__item_name": item_name,
            "__child_widget_div": child_widget_div,
        }

        self.add(
            preamble_hooks=[tpls.render("preamble_hooks_tpl", context)],
            preamble=[tpls.render("preamble_uniform_height_tpl", context)],
        )

    def _get_const_name(self):
        return f"{self.ilh.array_item_name}Divs"

    def update_widget_spec(self):
        self.ilh.update_widget_spec()
        append_uniq(self.widget_spec.root.div.attrs, tpls.render("div_attrs_tpl", {}))


def _get_child_widget_output(widget_spec, item_name, use_uniform_height):
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Child")
    with child_widget_spec.memo():
        child_widget_spec.div.key = f"{item_name}.id"
        if use_uniform_height:
            child_widget_spec.div.append_styles(
                [f"idx === {item_name}Idx ? 'visible' : 'invisible'"]
            )
        return build(child_widget_spec)


class StepperBackButtonBuilder(Builder):
    def build(self):
        pass


class StepperForwardButtonBuilder(Builder):
    def build(self):
        pass


preamble_hooks_tpl = chop0(
    """
{% magic_with __item_name as myItem %}
    const [myItemIdx, setMyItemIdx] = React.useState(0);

    const moveBack = React.useCallback(
      () =>
        setMyItemIdx(myItemIdx > 0 ? myItemIdx - 1 : {{ __items_expr }}.length - 1),
      [myItemIdx, setMyItemIdx, {{ __items_expr }}]
    );

    const moveForward = React.useCallback(
      () =>
        setMyItemIdx(myItemIdx < {{ __items_expr }}.length - 1 ? myItemIdx + 1 : 0),
      [myItemIdx, setMyItemIdx, {{ __items_expr }}]
    );
    {{ "" }}
{% end_magic_with %}
    """
)

preamble_uniform_height_tpl = chop0(
    """
const {{ __const_name }} = {{ __items_expr }}.map(({{ __item_name }}, idx) => {
  {{ __child_widget_div }}
});
"""
)

div_attrs_tpl = chop0(
    """
    tabIndex={123}
    onKeyDown={(e) => {
        if (e.key === 'ArrowLeft') moveBack();
        if (e.key === 'ArrowRight') moveForward();
    }}
"""
)

tpls = Tpls(
    "stepper_builder",
    preamble_hooks_tpl=preamble_hooks_tpl,
    preamble_uniform_height_tpl=preamble_uniform_height_tpl,
    div_attrs_tpl=div_attrs_tpl,
)
