import { EndpointData } from 'src/api/EndpointData';

export const loadingList = Object.freeze([]);

export const loadingObj = Object.freeze({});

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

export const createMaybe =
  (parentResource: any) =>
  (resource: any, defaultValue: any = null) =>
    isLoaded(parentResource) ? resource : _defaultValue(defaultValue);

const _defaultValue = (value: any) => {
  return Array.isArray(value)
    ? loadingList
    : value === null
    ? null
    : loadingObj;
};
