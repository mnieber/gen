import * as R from 'ramda';
import { matchPath } from 'react-router-dom';
import { ObjT } from 'src/utils/types';

export function getMatchingRoutes(routes: ObjT, pathname: string) {
  const matchingRoutes = [];
  for (const route of R.values(routes)) {
    if (
      matchPath(pathname, {
        path: route(),
        strict: false,
      })
    ) {
      matchingRoutes.push(route);
    }
  }
  return matchingRoutes;
}
