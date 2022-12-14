from moonleap import Tpls, chop0

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
