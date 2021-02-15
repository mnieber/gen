import { action, observable, computed, makeObservable } from 'mobx';
import { RST, resetRS } from 'utils/RST';
{{ res.javascript_import_lines }}

export class {{ res.name }} {

{% loop item_list in res.item_lists %}
{% set list_name=item_list.name %}
  @observable {{ list_name }}ById: {{ list_name|title }}ByIdT = {};
  @observable {{ list_name }}ByIdRS: RST = resetRS(); {% onlyif res.useRST %}
{% endloop %}

  constructor() {
    makeObservable(this);
  }

{{ res.actions }}
}
