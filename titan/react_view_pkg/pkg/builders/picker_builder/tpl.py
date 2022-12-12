from moonleap import Tpls, chop0

picker_handler_tpl = chop0(
    """
{% magic_with __.item as myItem %}
    const onChange = (value: PickerValueT) => {
      if (value.__isNew__) {
        // Moonleap Todo: add myItem
      } else if (value.value) {
        props.myItemsSelection.selectItem({                           {% if __.bvrs_has_selection %}
          itemId: value.value.id
        });
        props.myItemsHighlight.id = value.value.id;                   {% elif __.bvrs_has_highlight %}{% endif %}
        props.updateUrl && props.updateUrl(value.value);              {% ?? __.update_url %}
      }
    };
    {{ "" }}
{% end_magic_with %}
"""
)

picker_div_tpl = chop0(
    """
{% magic_with __.item as myItem %}
    <ValuePicker
        isMulti={false}
        isCreatable={true}
        pickableValues={ props.myItems }
        labelFromValue={(x: any) => x.name}
        pickableValue={props.myItemsHighlight.item}
        onChange={onChange}
    />
{% end_magic_with %}
"""
)

picker_imports_tpl = chop0(
    """
{% magic_with __.item as myItem %}
import { PickerValueT, ValuePicker } from 'src/utils/components/ValuePicker';
import { MyItemT } from 'src/api/types/MyItemT';                                {% ?? __.update_url %}
{% end_magic_with %}
    """
)

picker_props_tpl = chop0(
    """
{% magic_with __.item as myItem %}
    updateUrl?: (myItem: MyItemT) => void;                                      {% ?? __.update_url %}
{% end_magic_with %}
    """
)

tpls = Tpls(
    "picker_builder",
    picker_div_tpl=picker_div_tpl,
    picker_handler_tpl=picker_handler_tpl,
    picker_imports_tpl=picker_imports_tpl,
    picker_props_tpl=picker_props_tpl,
)
