import { action, makeObservable, observable } from 'mobx';
import { forEach } from 'ramda';
import { resetRS, RST } from 'src/utils/RST';

export class ResourceStateMap {
  @observable resourceStateByResUrl: { [key: string]: RST } = {};

  constructor() {
    makeObservable(this);
  }

  @action registerRS(state: RST, resUrls: string[]) {
    forEach((resUrl: string) => {
      this.resourceStateByResUrl[resUrl] = state;
    })(resUrls);
  }

  has(resUrl: string): boolean {
    return !!this.resourceStateByResUrl[resUrl];
  }

  get(resUrl: string): RST {
    return this.resourceStateByResUrl[resUrl] ?? resetRS();
  }
}

export const rsMap = new ResourceStateMap();

export const maybeResUrl = (getter: Function, ...args: any) => {
  for (var i = 0; i < args.length; ++i) {
    if (args[i] === undefined) {
      return undefined;
    }
  }
  return getter(...args);
};
