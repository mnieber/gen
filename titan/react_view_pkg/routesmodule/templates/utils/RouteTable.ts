import * as R from 'ramda';
import { generatePath } from 'react-router-dom';
import { ObjT } from 'src/utils/types';

export class RouteTable {
  routeByName: ObjT = {};
  _routes: ObjT = {};
  tableByPrefix: ObjT = {};

  addRoute(route: string, name: string, prefix: string = '') {
    if (this._routes[name] && this._routes[name] !== route) {
      throw new Error(`Route ${name} already exists, with a different value`);
    }

    this._routes[name] = route;
    this.routeByName[name] = (args?: ObjT) => {
      return R.isEmpty(args ?? {})
        ? prefix + route
        : generatePath(prefix + route, (args ?? {}) as ObjT);
    };
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
