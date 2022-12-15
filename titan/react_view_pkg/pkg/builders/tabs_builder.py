from moonleap import Tpls, chop0, u0
from moonleap.utils.fp import append_uniq, extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin
from titan.types_pkg.typeregistry import get_type_reg


class TabsBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _add_lines(self):
        has_uniform_height = bool(self.widget_spec.get_value_by_name("uniformHeight"))
        item_name = self.bvrs_item_name
        context = dict(__=self._get_context(has_uniform_height))
        context["__"]["tab_instance_div"] = self.output.graft(
            _get_tab_instance_output(
                self.widget_spec,
                div_attrs=None,
                div_styles=(
                    [f"{item_name}.id === {item_name}Id ? 'visible' : 'invisible'"]
                    if has_uniform_height
                    else []
                ),
                key=f"{item_name}.id",
            )
        )

        self.add(
            imports_lines=[tpls.render("tab_view_imports_tpl", context)],
            preamble_lines=[tpls.render("tab_view_preamble_tpl", context)],
            lines=[tpls.render("tab_view_div_tpl", context)],
        )

    def _get_context(self, has_uniform_height):
        type_spec = get_type_reg().get(u0(self.bvrs_item_name))

        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "items_expr": self.item_list_data_path(),
            "component_name": self.widget_spec.widget_class_name,
            "display_field_name": (
                type_spec.display_field.name if type_spec.display_field else None
            ),
            "uniform_tab_height": has_uniform_height,
        }


def _get_tab_instance_output(widget_spec, div_attrs, div_styles, key):
    # This returns the div that is used in the Tabs.
    # Don't confuse this with the div that is used in the TabsItem.
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Tab")
    with child_widget_spec.memo():
        child_widget_spec.div.key = key

        extend_uniq(child_widget_spec.div.styles, div_styles)
        if div_attrs:
            append_uniq(child_widget_spec.div.attrs, div_attrs)
        return build(child_widget_spec)


tab_view_imports_tpl = chop0(
    """
{% magic_with __.item_name as myItem %}
import React from 'react';
import { MyItemT } from 'src/api/types/MyItemT';
import { Tab, TabList, TabPanel, Tabs } from 'react-tabs';
import 'react-tabs/style/react-tabs.scss';
{% end_magic_with %}
"""
)

tab_view_preamble_tpl = chop0(
    """
{% magic_with __.item_name as myItem %}
    const [myItemId, setMyItemId] = React.useState<string>(
      props.myItems[0].id
    );

    const tabs = props.myItems.map((myItem: MyItemT) => {
      return (
        <Tab key={myItem.id} onClick={() => setMyItemId(myItem.id)}>
          { myItem.{{ __.display_field_name }} }                                                   {% ?? __.display_field_name %}
          Moonleap Todo                                                                            {% ?? not __.display_field_name %}
        </Tab>
      );
    });

    const tabPanels = props.myItems.map((myItem: MyItemT) => {
      return <TabPanel key={myItem.id}>
        {{ __.tab_instance_div }}                                                                  {% ?? not __.uniform_tab_height %}
      </TabPanel>;
    });

    const myItemDivs = props.myItems.map((myItem: MyItemT) => {                                    {% if __.uniform_tab_height %}
      {{ __.tab_instance_div }}
    });                                                                                            {% endif %}

    const noItems = (<h2 className="p-2">
      There are no {{ __.item_name|camel_to_kebab|plural }}
    </h2>);
{{ "" }}
{% end_magic_with %}
"""
)

tab_view_div_tpl = chop0(
    """
{% magic_with __.item_name as myItem %}
{% magic_with __.component_name as MyComponent %}
        <Tabs className="MyComponent">
          <TabList>{tabs}</TabList>
          {tabPanels}
        </Tabs>
        {myItemDivs.length === 0 && noItems}
        <div className={cn('CodeBlockTabView__Body')}>{myItemDivs}</div>
{% end_magic_with %}
{% end_magic_with %}
"""
)

tpls = Tpls(
    "tab_view_builder",
    tab_view_imports_tpl=tab_view_imports_tpl,
    tab_view_preamble_tpl=tab_view_preamble_tpl,
    tab_view_div_tpl=tab_view_div_tpl,
)
