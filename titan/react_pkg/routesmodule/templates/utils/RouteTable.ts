import * as R from 'ramda';
import { generatePath } from 'react-router-dom';
import { ObjT } from 'src/utils/types';
import { pathname } from 'src/utils/urls';

export class RouteTable {
  routeByName: ObjT = {};
  routeUfnByName: ObjT = {};
  _routes: ObjT = {};
  _routeUfns: ObjT = {};

  addRoute(route: string | Function, name: string, prefix: string = '') {
    if (this._routes[name]) {
      if (this._routes[name] !== route) {
        throw new Error(`Route ${name} already exists, with a different value`);
      }
    } else {
      this._routes[name] = route;
      this.routeByName[name] = (args?: ObjT) => {
        const routeStr = typeof route === 'function' ? route() : route;
        return R.isEmpty(args ?? {})
          ? prefix + routeStr
          : generatePath(prefix + routeStr, (args ?? {}) as ObjT);
      };
    }
  }

  addRouteUfn(name: string, getRouteArgs: Function) {
    if (this._routeUfns[name]) {
      if (this._routes[name] !== getRouteArgs) {
        throw new Error(
          `A routeUfn with ${name} already exists, with a different value`
        );
      }
    } else {
      this._routeUfns[name] = getRouteArgs;
      this.routeUfnByName[name] =
        (updateRoute: Function) =>
        (...args: any[]) => {
          const routeArgs = getRouteArgs(...args);
          const newRoute = this.routeByName[name](routeArgs);
          if (pathname() !== newRoute) {
            updateRoute(newRoute);
          }
        };
    }
  }

  addRoutes(routeByName: ObjT, prefix: string = '') {
    for (const name in routeByName) {
      const value = routeByName[name];
      const [route, getRouteArgs] = Array.isArray(value)
        ? value
        : [value, () => ({})];

      this.addRouteUfn(name, getRouteArgs);
      this.addRoute(route, name, prefix);
    }
  }

  addTable(table: RouteTable, prefix: string) {
    for (const [name, route] of Object.entries(table._routes)) {
      this.addRoute(route, name, prefix);
    }
    for (const [name, routeUfn] of Object.entries(table._routeUfns)) {
      this.addRouteUfn(name, routeUfn);
    }
  }
}
