import * as R from 'ramda';
import React from 'react';
import { Route as BaseRoute } from 'react-router-dom';
import { routeTable } from 'src/routes/routes';

type RoutePropsT = React.PropsWithChildren<{
  path: string;
  name?: string;
}>;

export const Route = (props: RoutePropsT) => {
  const { path, name } = props;
  if (name) {
    routeTable.addRoute(path, name);
  }

  return <BaseRoute {...R.omit(['name'], props)}>{props.children}</BaseRoute>;
};
