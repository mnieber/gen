import { action, makeObservable, observable } from 'mobx';
import { forEach } from 'lodash/fp';
import { resetRS, RST } from 'src/utils/RST';

export class ResourceStatesStore {
  @observable resourceStateByUrl: { [key: string]: RST } = {};

  constructor() {
    makeObservable(this);
  }

  @action registerState(state: RST, resourceUrls: string[]) {
    forEach(
      (resourceUrl: string) => (this.resourceStateByUrl[resourceUrl] = state)
    )(resourceUrls);
  }

  getState(resourceUrl: string): RST {
    return this.resourceStateByUrl[resourceUrl] ?? resetRS();
  }
}

export const rsStore = new ResourceStatesStore();
