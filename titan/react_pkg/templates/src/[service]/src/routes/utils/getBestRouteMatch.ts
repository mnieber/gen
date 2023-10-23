import * as R from 'ramda';
import { matchPath } from 'react-router-dom';
import { ObjT } from '/src/utils/types';

export type RouteMatchT = {
  path: string;
  name: string;
  params: ObjT;
};

export function getBestRouteMatch(
  routes: ObjT,
  pathname: string
): RouteMatchT | undefined {
  const bestMatch = {
    result: undefined as RouteMatchT | undefined,
    nrParams: 0,
  };

  for (const [name, route] of R.toPairs(routes)) {
    const match = matchPath(pathname, {
      path: route(),
      strict: false,
    });
    if (
      match?.isExact ||
      R.keys(match?.params ?? {}).length > bestMatch.nrParams
    ) {
      bestMatch.result = { ...match, name } as RouteMatchT;
      bestMatch.nrParams = R.keys(match?.params ?? {}).length;
    }
  }

  return bestMatch.result;
}
