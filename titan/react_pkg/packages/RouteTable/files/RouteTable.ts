import { ObjT } from 'src/utils/types';

export class RouteTable {
  routeByName: ObjT = {};
  tableByPrefix: ObjT = {};

  addRoute(route: Function, name: string, prefix: string = '') {
    this.routeByName[name] = prefix
      ? (...args: any[]) => prefix + route(...args)
      : route;
  }

  addRoutes(routeByName: ObjT, prefix: string = '') {
    for (const name in routeByName) {
      this.addRoute(routeByName[name], name, prefix);
    }
  }

  addTable(table: RouteTable, prefix: string) {
    this.addRoutes(table.routeByName, prefix);
  }
}
