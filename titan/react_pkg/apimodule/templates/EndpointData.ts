import { action, makeObservable, observable } from 'mobx';
import { ObjT } from 'src/utils/types';

export class EndpointData {
  @observable data: ObjT | undefined = undefined;
  @observable status: string = 'idle';

  constructor() {
    makeObservable(this);
  }

  @action clear = () => {
    this.data = undefined;
    this.status = 'idle';
  };
}
