import React from 'react';
import { RoutesContext } from 'src/routes/components/RoutesProvider';
import { RouteTable } from 'src/routes/utils/RouteTable';

export const useRouteTable = () => {
  const routeTable: RouteTable = React.useContext(RoutesContext);
  return routeTable;
};

export const useRoutes = () => {
  return useRouteTable().routeByName;
};
