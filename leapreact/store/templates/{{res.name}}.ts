import { action, observable, computed, makeObservable } from 'mobx';
{{ res.javascript_import_lines }}

export class {{ res.name }} {
{{ res.fields }}

  constructor() {
    makeObservable(this);
  }

{{ res.actions }}
}
