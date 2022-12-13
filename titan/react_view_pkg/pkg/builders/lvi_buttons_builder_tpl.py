from moonleap import Tpls, chop0

lvi_buttons_tpl = chop0(
    """
    <button
      className={smallButton}
      onClick={() => {
        props.onDelete();
      }}
    >
      Delete
    </button>
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
