import { action, observable, computed, makeObservable } from 'mobx';
import { forEach } from 'lodash/fp';
import { RST, resetRS, updateRes } from 'utils/RST';
import * as {{ res.module.name }}Api from "src/{{ res.module.name }}/api"

{% loop item_list in res.item_lists %}
import { {{ item_list.item_name|title }}T } from "src/{{ res.module.name }}/types"
{% endloop %}

{{ res.javascript_import_lines }}

export class {{ res.name }} {

{% loop item_list in res.item_lists %}
  @observable {{ item_list.item_name|byId }}: {{ item_list.item_name|byId|title }}T = {};
  @observable {{ item_list.item_name|byId }}RS: RST = resetRS();
{% endloop %}

  constructor() {
    makeObservable(this);
  }

{% loop item_list in res.item_lists %}
  @action load{{ items|title }} = () => {
    updateRes(
      this,
      '{{ item_list.item_name|byId }}',
      () => {
        return {{ res.module.name }}Api.get{{ item_list.item_name|plural|title }}();
      },
      (response: any) => {
        this.add{{ item_list.item_name|plural|title }}(response.{{ item_list.item_name|plural }});
      },
      (message: any) => {
        console.log(message);
        return 'Oops, there was an error getting the {{ items }} data';
      }
    );
  }
  {{ res and "" }}
  @action add{{ items|title }} = ({{ items }}: {{ item_list.item_name|title }}T[]) => {
    forEach(({{ item_list.item_name }}) => {
      this.{{ item_list.item_name|byId }}[{{ item_list.item_name }}.uuid] = {{ item_list.item_name }};
    }, {{ item_list.item_name|plural }});
  }
{% endloop %}

}
