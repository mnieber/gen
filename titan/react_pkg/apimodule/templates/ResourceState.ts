import { action, makeObservable, observable } from 'mobx';
import { EndpointData } from 'src/api/EndpointData';

export const symbolRS = Symbol('ResourceState');
export const loadingList = Object.freeze([]);
export const loadingObj = Object.freeze({});

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

export function isLoading(resource: any) {
  if (resource instanceof EndpointData) {
    return resource.status === 'idle' || resource.status === 'loading';
  }
  return (
    resource === null || resource === loadingList || resource === loadingObj
  );
}

export function isLoaded(resource: any) {
  return !isLoading(resource);
}

export const maybe =
  (parentResource: any, defaultValue: any = null) =>
  (resource: any) =>
    isLoaded(parentResource) ? resource : _defaultValue(defaultValue);

const _defaultValue = (value: any) => {
  return Array.isArray(value)
    ? loadingList
    : value === null
    ? null
    : loadingObj;
};
