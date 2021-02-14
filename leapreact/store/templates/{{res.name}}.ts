import { action, observable, computed, makeObservable } from 'mobx';
import { RST, resetRS } from 'utils/RST';
{{ res.javascript_import_lines }}

export class {{ res.name }} {
{% for item_list in res.item_lists %}
  @observable {{ item_list.name }}ById: {{ item_list.name|title }}ByIdT = {};
{% if res.useRST %}
  @observable {{ item_list.name }}ByIdRS: RST = resetRS();
{% endif %}
{% endfor %}
{{ res.fields }}

  constructor() {
    makeObservable(this);
  }

{{ res.actions }}
}
