from moonleap import Tpls, chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.array_builder import ArrayBuilder


class StepperBuilder(ArrayBuilder):
    def build(self):
        context = {
            "__items_expr": self.ilh.item_list_data_path(),
            "__item_name": self.ilh.array_item_name,
        }
        self.add(
            preamble_hooks_lines=[tpls.render("preamble_hooks_tpl", context)],
        )
        return super().build()

    def _get_const_name(self):
        return f"{self.ilh.array_item_name}Divs"


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
      [myItemIdx, setMyItemIdx, {{ __items_expr }}.length]
    );
    {{ "" }}
{% end_magic_with %}
    """
)

tpls = Tpls(
    "stepper_builder",
    preamble_hooks_tpl=preamble_hooks_tpl,
)
