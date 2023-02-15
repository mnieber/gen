import * as R from 'ramda';

export const symbolRS = Symbol('ResourceState');

export type ResourceStateT = undefined | 'loading' | 'updating' | 'ready';

export const isUpdating = (resource: any) => getState(resource) === 'updating';
export const isLoading = (resource: any) =>
  resource === null || getState(resource) === 'loading';
export const isReady = (resource: any) => getState(resource) === 'ready';
export const isUndefined = (resource: any) =>
  resource === undefined || getState(resource) === undefined;

export const setState = (resource: any, state: ResourceStateT) => {
  resource[symbolRS] = state;
};

export const setToUpdating = (resource: any) => setState(resource, 'updating');
export const setToLoading = (resource: any) => setState(resource, 'loading');
export const setToReady = (resource: any) => setState(resource, 'ready');
export const setToUndefined = (resource: any) => setState(resource, undefined);

export const getState = (resource: any): ResourceStateT | undefined => {
  return resource ? resource[symbolRS] ?? undefined : undefined;
};

export const initRS = (resource: any, state?: ResourceStateT) => {
  if (resource && R.isNil(resource[symbolRS])) {
    resource[symbolRS] = state ?? undefined;
  }
  return resource;
};
