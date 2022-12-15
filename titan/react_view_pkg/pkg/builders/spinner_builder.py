from moonleap import Tpls, chop0
from titan.react_view_pkg.pkg.builder import Builder

uikit_tpl = chop0(
    """
    if (!isLoaded({{ data_path }})) {
        return UIkit && <div data-uk-spinner className="" />;
    }
    else if ({{ test }}) return null;                                             {% ?? guard %}
    {{ "" }}
"""
)

no_uikit_tpl = chop0(
    """
    if (!isLoaded({{ data_path }})) {
        return null;
    }
    else if ({{ test }}) return null;                                             {% ?? guard %}
    {{ "" }}
"""
)

tpls = Tpls("spinner_builder", uikit_tpl=uikit_tpl, no_uikit_tpl=no_uikit_tpl)


class SpinnerBuilder(Builder):
    def build(self):
        tpl = "uikit_tpl" if self.use_uikit else "no_uikit_tpl"
        item_list_data_path = self.ilh.item_list_data_path()
        item_data_path = self.ih.item_data_path()

        context = {
            "test": (
                f"!{item_list_data_path}?.length"
                if item_list_data_path
                else f"!{item_data_path}"
            ),
            "data_path": item_list_data_path or item_data_path,
            "guard": self.widget_spec.get_value_by_name("guard"),
        }

        self.add(preamble_lines=[tpls.render(tpl, context)])
