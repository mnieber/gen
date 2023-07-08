import * as R from 'ramda';
import {
  initRS,
  isLoading,
  isUpdating,
  ResourceStateT,
  setState,
  symbolRS,
} from '/src/api/ResourceState';

export type OptionsT = {
  debugLabel?: string;
};

export const cloneAndSetState = (
  resource: any,
  sources: any[],
  options?: OptionsT
) => {
  if (resource === null) {
    if (options?.debugLabel) {
      console.log(
        `cloneAndSetState: ${options?.debugLabel} - resource is null`
      );
    }
    return resource;
  }

  let resultState: ResourceStateT = undefined;

  for (const source of sources) {
    let [srcState, srcRes, srcLabel] = source;
    if (Array.isArray(srcRes)) {
      const [endpoint, flag] = srcRes;
      if (!flag) {
        continue;
      }
      srcRes = initRS({});
      srcLabel = srcLabel ?? endpoint.toString();

      const isEndpointLoading =
        endpoint.status === 'loading' ||
        (endpoint.status === 'idle' && srcState === 'loading');
      setState(srcRes, isEndpointLoading ? srcState : 'ready');
    }

    if (srcState === 'loading' && isLoading(srcRes)) {
      resultState = srcState;
      options?.debugLabel &&
        console.log(
          `cloneAndSetState: ${options?.debugLabel} - source ${srcLabel} is loading`
        );
      break;
    }

    if (srcState === 'updating' && isUpdating(srcRes)) {
      resultState = srcState;
      options?.debugLabel &&
        console.log(
          `cloneAndSetState: ${options?.debugLabel} - source ${srcLabel} is updating`
        );
      break;
    }
  }

  if (R.isNil(resource)) {
    return resultState === 'loading' ? null : undefined;
  }

  // Check if the existing resource is loading or updating. In that case,
  // the state of the existing resource takes precedence.
  const currentState = (resource as any)[symbolRS];
  if (currentState === 'loading' || currentState === 'updating') {
    options?.debugLabel &&
      console.log(
        `cloneAndSetState: ${options?.debugLabel} - currentlyLoadingOrUpdating=true`
      );
    resultState = currentState;
  }

  // Clone the resource
  const result = Array.isArray(resource) ? [...resource] : { ...resource };
  (result as any)[symbolRS] = resultState;
  return result;
};
