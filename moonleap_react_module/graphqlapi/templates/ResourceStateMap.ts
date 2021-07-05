import { action, makeObservable, observable } from 'mobx';
import { forEach } from 'ramda';
import { resetRS, RST } from 'src/utils/RST';

export class ResourceStateMap {
  @observable resourceStateByResUrl: { [key: string]: RST } = {};

  constructor() {
    makeObservable(this);
  }

  @action registerState(state: RST, resourceUrls: string[]) {
    forEach(
      (resUrl: string) => {this.resourceStateByResUrl[resUrl] = state}
    )(resourceUrls);
  }

  getState(resUrl: string): RST {
    return this.resourceStateByResUrl[resUrl] ?? resetRS();
  }
}

export const rsMap = new ResourceStateMap();
