import React from 'react';
import { makeObservable, observable } from 'mobx';
{% for substore in res.substores %}
import { {{ substore.name }} } from "{{ substore.import_path }}/{{ substore.name }}"
{% endfor %}


class GlobalStore {
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

const globalStore = new GlobalStore();

const StoreContext = React.createContext<GlobalStore>(globalStore);

export const StoreProvider: React.FC = ({ children }) => {
  return (
    <StoreContext.Provider value={globalStore}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => {
  const store = React.useContext(StoreContext);
  if (!store) {
    throw new Error('useStore must be used within a StoreProvider.');
  }
  return store;
};
