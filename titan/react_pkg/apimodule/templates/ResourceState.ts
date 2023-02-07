import * as R from 'ramda';
import { EndpointData } from 'src/api/EndpointData';

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

export type RegOptionsT = {
  loading?: any[];
  updating?: any[];
};

export const cloneAndSetState = (resource: any, options: RegOptionsT) => {
  if (resource === null) {
    return resource;
  }

  let state: ResourceStateT = undefined;

  for (const source of options.loading ?? []) {
    if (source !== undefined && isLoading(source)) {
      state = 'loading';
      break;
    }
  }

  if (!state) {
    for (const source of options.updating ?? []) {
      if (source !== undefined && isUpdating(source)) {
        state = 'updating';
        break;
      }
    }
  }

  if (R.isNil(resource)) {
    return state === 'loading' ? null : undefined;
  }

  const result = Array.isArray(resource) ? [...resource] : { ...resource };
  const currentState = (resource as any)[symbolRS];
  // When we set the result RS, then a "loading" or "updating" state from the
  // input "resource" takes precedence.
  (result as any)[symbolRS] =
    currentState === 'loading' || currentState === 'updating'
      ? currentState
      : state;
  return result;
};

export const maybe = (
  endpoint: EndpointData,
  state: ResourceStateT,
  flag: boolean
) => {
  const result = initRS({});

  if (flag) {
    const isEndpointLoading =
      endpoint.status === 'loading' ||
      (endpoint.status === 'idle' && state === 'loading');
    setState(result, isEndpointLoading ? state : 'ready');
  }

  return result;
};
