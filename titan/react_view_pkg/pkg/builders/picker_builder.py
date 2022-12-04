from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder

on_change_template_str = chop0(
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

"""
)

div_template_str = chop0(
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

div_imports_str = chop0(
    """
import { PickerValueT, ValuePicker } from 'src/utils/components/ValuePicker';
    """
)


class PickerBuilder(Builder):
    def build(self, div_attrs):
        item_name = self.item_list.item.item_name
        items_name = plural(item_name)

        packages = self.output.react_packages_by_module_name.setdefault("utils", [])
        extend_uniq(packages, ["ValuePicker"])

        append_uniq(self.output.default_props, f"{items_name}:selection")
        append_uniq(self.output.default_props, f"{items_name}:highlight")
        handler_code = get_template_from_str(on_change_template_str).render(
            {"item": item_name}
        )
        self.add_preamble_lines([handler_code])
        self.add_import_lines([div_imports_str])

        div = get_template_from_str(div_template_str).render({"item": item_name})
        self.add_lines([div])
