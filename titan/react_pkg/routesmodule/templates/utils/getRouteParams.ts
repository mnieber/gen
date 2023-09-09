import { getRouteMatch } from '/src/routes/utils/getRouteMatch';

export const getRouteParams = () => {
  return getRouteMatch()?.params ?? {};
};
