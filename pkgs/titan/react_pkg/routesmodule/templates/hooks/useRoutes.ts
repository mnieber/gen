import React from 'react';
import { useHistory } from 'react-router-dom';
import { RoutesContext } from 'src/routes/components/RoutesProvider';
import { RouteTable } from 'src/routes/utils/RouteTable';

export const useRouteTable = () => {
  const routeTable: RouteTable = React.useContext(RoutesContext);
  return routeTable;
};

export const useRoutes = () => {
  return useRouteTable().routeByName;
};

export const useRouteUfns = () => {
  const history = useHistory();
  return { routeUfns: useRouteTable().routeUfnByName, history };
};
