import * as R from 'ramda';
import React from 'react';
import { Route as BaseRoute } from 'react-router-dom';
import { useRouteTable } from 'src/routes/hooks/useRoutes';
import { ObjT } from 'src/utils/types';

type RoutePropsT = React.PropsWithChildren<{
  path: string;
  exact?: boolean;
  name?: string;
}>;

export const Route = (props: RoutePropsT) => {
  const routeTable = useRouteTable();

  const { path, name } = props;
  if (name) {
    routeTable.addRoute(path, name);
  }

  return (
    <BaseRoute {...(R.omit(['name'], props) as ObjT)}>
      {props.children as any}
    </BaseRoute>
  );
};
