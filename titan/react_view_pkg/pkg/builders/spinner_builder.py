from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

uikit_tpl = chop0(
    """
    if ({{ data_path }} == undefined) return null;                          {% ?? guard %}
    if (!isLoaded({{ data_path }})) {
        return UIkit && <div data-uk-spinner className="" />;
    }
    {{ "" }}
"""
)

no_uikit_tpl = chop0(
    """
    if (
        {{ data_path }} == undefined ||                                     {% ?? guard %}
        !isLoaded({{ data_path }})
    ) {
        return null;
    }
    {{ "" }}
"""
)


class SpinnerBuilder(Builder):
    def build(self):
        tpl = uikit_tpl if self.use_uikit else no_uikit_tpl
        item_list_data_path = self.item_list_data_path()
        item_data_path = self.item_data_path()

        context = {
            "test": (
                f"!{item_list_data_path}?.length"
                if item_list_data_path
                else f"!{item_data_path}"
            ),
            "data_path": item_list_data_path or item_data_path,
            "guard": self.get_value_by_name("guard"),
        }

        self.add(preamble_lines=[self.render_str(tpl, context, "spinner_builder.j2")])
