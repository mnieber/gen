import React from 'react';
import { RoutesContext } from 'src/routes/components/RoutesProvider';
import { history } from 'src/routes/components/UrlRouter';
import { RouteTable } from 'src/routes/utils/RouteTable';

export const useRouteTable = () => {
  const routeTable: RouteTable = React.useContext(RoutesContext);
  return routeTable;
};

export const useRoutes = () => {
  return useRouteTable().routeByName;
};

export const useRouteUfns = () => {
  return { routeUfns: useRouteTable().routeUfnByName, history };
};
