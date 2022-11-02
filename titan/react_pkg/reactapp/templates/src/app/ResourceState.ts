import { action, makeObservable, observable } from 'mobx';

export const symbolRS = Symbol('ResourceState');

export class ResourceState {
  @observable _isUpdating: boolean = false;

  @action setIsUpdating(isUpdating: boolean) {
    this._isUpdating = isUpdating;
  }

  isUpdating() {
    return this._isUpdating;
  }

  constructor() {
    makeObservable(this);
  }
}

export const isUpdating = (x: any) => getRS(x).isUpdating();

export const setToUpdating = (x: any) => getRS(x).setIsUpdating(true);

export const setToIdle = (x: any) => getRS(x).setIsUpdating(false);

export const getRS = (x: any) => x[symbolRS];

export const initRS = (x: any) => {
  x[symbolRS] = x[symbolRS] ?? new ResourceState();
};
