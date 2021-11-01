import * as R from 'ramda';
import { generatePath, matchPath } from 'react-router-dom';
import { routes } from 'src/routes/routes';

export function createNavigateTo(
  renderedRoute: any,
  getParamsFromItem: Function
) {
  return (item: any) => {
    if (!item) {
      return;
    }

    const loc = window.location.pathname;
    for (const route of R.values(routes)) {
      const path = route();
      const match = matchPath(loc, path);
      if (match?.isExact) {
        const newUrl = generatePath(path, {
          ...match.params,
          ...getParamsFromItem(item),
        });
        if (newUrl !== loc) {
          window.history.replaceState(null, '', newUrl);
        }
      }
    }
  };
}
