import React from 'react';

import { observable, action } from 'mobx';

export class MobXFormState {
  @observable values: any[];

  constructor(values: any[]) {
    this.values = values;
  }

  @action setValues = (values: any[]) => {
    for (const prop of Object.getOwnPropertyNames(values)) {
      this.values[prop as any] = values[prop as any];
    }
  };
}

export const useMobXState = (initialValues: any) => {
  const [container] = React.useState<MobXFormState>(
    () => new MobXFormState(initialValues)
  );
  return [container.values, container.setValues];
};
