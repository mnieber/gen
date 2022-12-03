from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

uikit_template_str = chop0(
    """
    if ({{ test }}) {
      return !isLoaded({{ get_res_expr }})
        ? UIkit && <div data-uk-spinner className="" />
        : null;
    }

"""
)

no_uikit_template_str = chop0(
    """
    if ({{ test }}) {
      return null;
    }

"""
)


class SpinnerBuilder(Builder):
    def build(self, div_attrs=None):
        use_ui_kit = True  # TODO
        template_str = uikit_template_str if use_ui_kit else no_uikit_template_str
        res = self.item or self.item_list
        data_path = self.item_list_data_path() or self.item_data_path()

        code = get_template_from_str(template_str).render(
            {
                "test": f"!props.{res.ts_var}",
                "get_res_expr": data_path,
            }
        )
        self.output.preamble_lines.extend([code])
