import React from 'react';
{% for substore in res.substores %}
import { {{ substore.name }} } from "{{ substore.import_path }}"
{% endfor %}

class AppStore {
{% for substore in res.substores %}
  @observable {{ substore.var_name }}: {{ substore.name }};
{% endfor %}

  constructor() {
    makeObservable(this);

{% for substore in res.substores %}
    this.{{ substore.var_name }} = new {{ substore.name }}();
{% endfor %}

    this.applyPolicies();
  }

  applyPolicies() {
{{ res.policy_lines }}
  }
}
