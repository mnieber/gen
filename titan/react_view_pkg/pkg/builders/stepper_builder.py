from moonleap import Tpls, chop0
from moonleap.utils.fp import append_uniq, extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin


class StepperBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "items_expr": self.item_list_data_path(),
            "component_name": self.widget_spec.widget_class_name,
        }

    def _add_lines(self):
        context = self._get_context()
        self.add(
            preamble_hooks_lines=[tpls.render("preamble_hooks_tpl", context)],
        )


class StepperBackButtonBuilder(Builder):
    def build(self):
        pass


class StepperForwardButtonBuilder(Builder):
    def build(self):
        pass


preamble_hooks_tpl = chop0(
    """
{% magic_with item_name as myItem %}
    const [myItemIdx, setMyItemIdx] = React.useState(0);

    const moveBack = React.useCallback(
      () =>
        setMyItemIdx(myItemIdx > 0 ? myItemIdx - 1 : {{ items_expr }}.length - 1),
      [myItemIdx, setMyItemIdx, {{ items_expr }}]
    );

    const moveForward = React.useCallback(
      () =>
        setMyItemIdx(myItemIdx < {{ items_expr }}.length - 1 ? myItemIdx + 1 : 0),
      [myItemIdx, setMyItemIdx, {{ items_expr }}.length]
    );
{% end_magic_with %}
    """
)

tpls = Tpls(
    "stepper_builder",
    preamble_hooks_tpl=preamble_hooks_tpl,
)
