import { action, makeObservable, observable } from 'mobx';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export class MobXFormState {
  @observable values: any[];

  constructor(values: any[]) {
    makeObservable(this);
    this.values = values;
  }

  @action setValues = (values: any[]) => {
    for (const prop of Object.getOwnPropertyNames(values)) {
      this.values[prop as any] = values[prop as any];
    }
  };
}

export const useMobXState = (initialValues: any) => {
  const container = useBuilder<MobXFormState>(
    () => new MobXFormState(initialValues)
  );
  return [container.values, container.setValues];
};
