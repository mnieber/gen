from moonleap import Tpls, chop0

picker_handler_tpl = chop0(
    """
    const onChange = (value: PickerValueT) => {
      if (value.__isNew__) {
        // Moonleap Todo: add {{ item }}
      } else if (value.value) {
        props.{{ item|plural }}Selection.selectItem({                           {% if bvrs_has_selection %}
          itemId: value.value.id
        });
        props.{{ item|plural }}Highlight.id = value.value.id;                   {% elif bvrs_has_highlight %}{% endif %}
      }
    };
    {{ "" }}
"""
)

picker_div_tpl = chop0(
    """
    <ValuePicker
        isMulti={false}
        isCreatable={true}
        pickableValues={ props.{{ item|plural }} }
        labelFromValue={(x: any) => x.name}
        pickableValue={props.{{ item|plural }}Highlight.item}
        onChange={onChange}
    />
"""
)

picker_imports_tpl = chop0(
    """
import { PickerValueT, ValuePicker } from 'src/utils/components/ValuePicker';
    """
)

tpls = Tpls(
    "picker_builder",
    picker_div_tpl=picker_div_tpl,
    picker_handler_tpl=picker_handler_tpl,
    picker_imports_tpl=picker_imports_tpl,
)
