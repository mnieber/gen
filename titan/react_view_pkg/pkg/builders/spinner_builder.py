from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

uikit_tpl = chop0(
    """
    if ({{ test }}) {
      return !isLoaded({{ get_res_expr }})
        ? UIkit && <div data-uk-spinner className="" />
        : null;
    }

"""
)

no_uikit_tpl = chop0(
    """
    if ({{ test }}) {
      return null;
    }

"""
)


class SpinnerBuilder(Builder):
    def build(self):
        tpl = uikit_tpl if self.use_uikit else no_uikit_tpl
        res = self.item or self.item_list
        data_path = self.item_list_data_path() or self.item_data_path()

        context = {
            "test": f"!props.{res.ts_var}",
            "get_res_expr": data_path,
        }

        code = self.render_str(tpl, context, "spinner_builder.j2")
        self.output.preamble_lines.extend([code])
