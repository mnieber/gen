from moonleap.utils import chop0
from moonleap.utils.fp import append_uniq, extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder

handler_tpl = chop0(
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

div_tpl = chop0(
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
    def __post_init__(self):
        self.item_name = self.named_item_list_term.data
        self.items_name = plural(self.item_name)

    def build(self):
        packages = self.output.react_packages_by_module_name.setdefault("utils", [])
        extend_uniq(packages, ["ValuePicker"])

        append_uniq(self.output.default_props, f"{self.items_name}:selection")
        append_uniq(self.output.default_props, f"{self.items_name}:highlight")

        context = {"item": self.item_name}

        if True:
            handler_code = self.render_str(
                handler_tpl, context, "picker_builder_handler.j2"
            )
            self.add_preamble_lines([handler_code])

        if True:
            self.add_import_lines([div_imports_str])

        if True:
            div = self.render_str(div_tpl, context, "picker_builder_div.j2")
            self.add_lines([div])
