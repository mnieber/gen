import { nullResource, symbolRS } from '/src/resourceStates/ResourceState';

export const getState = <StateT = string>(resource: any): StateT[] => {
  if (!!resource && !resource[symbolRS]) {
    debugger;
  }

  if (resource === undefined) {
    return [];
  }

  return resource === nullResource ? ['loading'] : resource[symbolRS].value;
};

export const isUpdating = (resource: any) =>
  getState(resource).includes('updating');
export const isLoading = (resource: any) =>
  getState(resource).includes('loading');
export const isReady = (resource: any) => {
  const state = getState(resource);
  return resource && !state.includes('loading') && !state.includes('updating');
};
export const isUndefined = (resource: any) =>
  resource === undefined || getState(resource).length === 0;
