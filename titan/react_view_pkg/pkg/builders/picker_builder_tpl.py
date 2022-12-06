from moonleap.utils import chop0

picker_handler_tpl = chop0(
    """
    const onChange = (value: PickerValueT) => {
      if (value.__isNew__) {
        // Moonleap Todo: add {{ item }}
      } else if (value.value) {
        props.{{ item|plural }}Selection.selectItem({
          itemId: value.value.id
        });
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
