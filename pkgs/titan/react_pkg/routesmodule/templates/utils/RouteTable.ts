import * as R from 'ramda';
import { generatePath } from 'react-router-dom';
import { ObjT } from 'src/utils/types';

export class RouteTable {
  routeByName: ObjT = {};
  _routes: ObjT = {};
  tableByPrefix: ObjT = {};

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

  addRoutes(routeByName: ObjT, prefix: string = '') {
    for (const name in routeByName) {
      this.addRoute(routeByName[name], name, prefix);
    }
  }

  addTable(table: RouteTable, prefix: string) {
    for (const [name, route] of Object.entries(table._routes)) {
      this.addRoute(route, name, prefix);
    }
  }
}
