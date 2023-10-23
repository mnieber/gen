import { action, computed, makeObservable, observable } from 'mobx';
import * as R from 'ramda';
import { generatePath } from 'react-router-dom';
import { ObjT } from '/src/utils/types';
import { pathname } from '/src/utils/urls';

export type RouteFnByNameT<T = any> = {
  [P in keyof T]: (args?: unknown) => string;
};
export type RouteUfnResultT = { route: string; changed: boolean };
export type RouteUfnByNameT<T = any> = {
  [P in keyof T]: T[P] extends (...args: infer A) => infer R
    ? (updateRoute: Function) => (...args: A) => RouteUfnResultT
    : never;
};

export type RouteSpecT = {
  path: string | Function;
  name: string;
  prefix: string;
  getRouteArgs: Function;
};

export class RouteTable {
  @observable _routeSpecByName: { [name: string]: RouteSpecT } = {};

  @computed get routeFnByName(): RouteFnByNameT {
    const result: RouteFnByNameT = {};
    for (const route of R.values(this._routeSpecByName)) {
      result[route.name] = (args?: unknown) => {
        const pathStr =
          typeof route.path === 'function' ? route.path() : route.path;
        return R.isEmpty(args ?? {})
          ? route.prefix + pathStr
          : generatePath(route.prefix + pathStr, args!);
      };
    }
    return result;
  }

  @computed get routeUfnByName(): RouteUfnByNameT {
    const result: RouteUfnByNameT = {};
    for (const routeSpec of R.values(this._routeSpecByName)) {
      result[routeSpec.name] = (updateRoute: Function) => (args: unknown) => {
        const routeArgs = routeSpec.getRouteArgs(args);
        const newRoute = this.routeFnByName[routeSpec.name](routeArgs);
        const changed = pathname() !== newRoute;
        if (changed) {
          updateRoute(newRoute);
        }
        return {
          route: newRoute,
          changed,
        };
      };
    }
    return result;
  }

  _addRouteSpec(routeSpec: RouteSpecT) {
    if (this._routeSpecByName[routeSpec.name]) {
      if (this._routeSpecByName[routeSpec.name].path !== routeSpec.path) {
        throw new Error(
          `Route ${routeSpec.name} already exists, with a different path`
        );
      }
    } else {
      this._routeSpecByName[routeSpec.name] = routeSpec;
    }
  }

  @action addRoutes(routeFnByName: ObjT, prefix: string = '') {
    for (const name in routeFnByName) {
      const value = routeFnByName[name];
      // By default, the getRouteArgs function is the identity function.
      // However, the caller can also pass in a function that transforms the
      // args object into a new args object.
      const [path, getRouteArgs] = Array.isArray(value)
        ? value
        : [value, (args: ObjT) => args];

      this._addRouteSpec({ name, prefix, path, getRouteArgs });
    }
  }

  @action addTable(table: RouteTable, prefix: string = '') {
    for (const routeSpec of R.values(table._routeSpecByName)) {
      this._addRouteSpec({
        name: routeSpec.name as string,
        prefix: prefix + routeSpec.prefix,
        path: routeSpec.path,
        getRouteArgs: routeSpec.getRouteArgs,
      });
    }
  }

  constructor() {
    makeObservable(this);
  }
}
