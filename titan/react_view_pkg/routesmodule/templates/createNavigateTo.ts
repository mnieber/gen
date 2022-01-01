import * as R from 'ramda';
import { generatePath } from 'react-router-dom';
import { routes } from 'src/routes/routes';
import { ObjT } from 'src/utils/types';

function _getNrOfMatchedParams(path: string, paramNames: string[]): number {
  let result = 0;
  for (const paramName of paramNames) {
    if (path.includes(`:${paramName}`)) {
      result += 1;
    }
  }
  return result;
}

function safeGeneratePath(path: string, params: ObjT) {
  try {
    return generatePath(path, params);
  } catch {
    return undefined;
  }
}

export function createNavigateTo(
  renderedRoute: any,
  getParamsFromItem: Function
) {
  return (item: any) => {
    if (!item) {
      return;
    }

    const params = {
      ...renderedRoute.params,
      ...getParamsFromItem(item),
    };

    let bestUrl = undefined;
    let bestNrOfMatchedParams = 0;

    for (const route of R.values(routes)) {
      const path = route();
      if (path.startsWith(renderedRoute.path)) {
        const newUrl = safeGeneratePath(path, params);

        if (newUrl && !newUrl.includes(':')) {
          const nrOfMatchedParams = _getNrOfMatchedParams(
            path,
            R.keys(params) as string[]
          );
          if (
            bestUrl === undefined ||
            nrOfMatchedParams > bestNrOfMatchedParams
          ) {
            bestUrl = newUrl;
            bestNrOfMatchedParams = nrOfMatchedParams;
          }
        }
      }
    }
    if (bestUrl && bestUrl !== window.location.pathname) {
      window.history.pushState(null, '', bestUrl);
    }
  };
}
