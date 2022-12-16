from moonleap import Tpls, chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper


class LviButtonsBuilder(Builder):
    def __post_init__(self):
        self.bvrs_helper = BvrsHelper(self.widget_spec, self.ilh.array_item_name)

    def build(self):
        context = self._get_context()

        self.add(
            lines=[tpls.render("lvi_buttons_tpl", context)],
            imports=[tpls.render("lvi_buttons_imports_tpl", context)],
            preamble=[tpls.render("lvi_buttons_preamble_tpl", context)],
            props=[tpls.render("lvi_buttons_props_tpl", context)],
        )

    def _get_context(self):
        return {
            **self.bvrs_helper.bvrs_context(),
            "item_name": self.ih.array_item_name,
            "component_name": self.widget_spec.widget_class_name,
            "uikit": self.use_uikit,
        }


lvi_buttons_tpl = chop0(
    """
    <button                                                                             {% if bvrs_has_deletion %}
      className={smallButton}
      onClick={() => {
        props.onDelete();
      }}
    >
      Delete
    </button>                                                                           {% endif %}
    """
)

lvi_buttons_props_tpl = chop0(
    """
onDelete: Function;                                                                     {% ?? bvrs_has_deletion %}
  """
)

lvi_buttons_preamble_tpl = chop0(
    """
{% magic_with item_name as myItemName %}
if (isUpdating(props.myItemName)) {
  return UIkit && <div data-uk-spinner className=""></div>;                             {% ?? uikit %}
  return null;                                                                          {% ?? not uikit %}
}
{{ "" }}
{% end_magic_with %}
  """
)

lvi_buttons_imports_tpl = chop0(
    """
import { smallButton } from 'src/frames/components';
  """
)

tpls = Tpls(
    "lvi_buttons_builder",
    lvi_buttons_tpl=lvi_buttons_tpl,
    lvi_buttons_props_tpl=lvi_buttons_props_tpl,
    lvi_buttons_preamble_tpl=lvi_buttons_preamble_tpl,
    lvi_buttons_imports_tpl=lvi_buttons_imports_tpl,
)
