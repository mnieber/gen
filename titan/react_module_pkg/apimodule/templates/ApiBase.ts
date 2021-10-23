import { Signal } from 'micro-signals';
import { pathOr } from 'ramda';
import { LoadDataEventT } from 'src/api/events';
import { flags } from 'src/app/flags';
import { doQuery } from 'src/utils/graphqlClient';
import { log } from 'src/utils/logging';
import { erroredRS, loadingRS, updatedRS } from 'src/utils/RST';
import { isString, ObjT } from 'src/utils/types';

export const defaultGetErrorMsg = (error: any) => {
  return pathOr(error, ['error', 'response', 'errors', 0, 'message'])(error);
};

export const defaultGetData = (response: any) => response;

export class ApiBase {
  signal: Signal<any> = new Signal();

  _dispatchUpdating(queryName: string, vars: ObjT) {
    this.signal.dispatch({
      topic: `Updating.${queryName}`,
      payload: {
        state: loadingRS(),
        vars,
      },
    } as LoadDataEventT);
  }

  _dispatchUpdated(queryName: string, vars: ObjT, data: any) {
    this.signal.dispatch({
      topic: `Updated.${queryName}`,
      payload: {
        vars,
        data,
        state: updatedRS(),
      },
    } as LoadDataEventT);
  }

  _dispatchErrored(queryName: string, vars: ObjT, error: string) {
    this.signal.dispatch({
      topic: `Errored.${queryName}`,
      payload: {
        vars,
        state: erroredRS(error),
      },
    } as LoadDataEventT);
  }

  doQuery(
    queryName: string,
    query: string | (() => any),
    vars: ObjT,
    getData: Function | undefined = undefined,
    getErrorMsg: (error: ObjT) => string = defaultGetErrorMsg
  ) {
    if (flags.logQueries) {
      log(`Query started: ${queryName}`, vars);
    }

    this._dispatchUpdating(queryName, vars);

    const result = (
      isString(query)
        ? doQuery(query as string, vars)
        : Promise.resolve((query as any)() ?? {})
    ).then((response) => {
      return {
        response,
        data: (getData ?? defaultGetData)(response),
      };
    });

    result
      .then(({ response, data }) => {
        if (flags.logQueries) {
          log(`Query finished: ${queryName}`, vars, response);
        }

        if (data instanceof Error) {
          this._dispatchErrored(queryName, vars, data.message);
        } else {
          this._dispatchUpdated(queryName, vars, data);
        }
      })
      .catch((error) => {
        if (flags.logQueries) {
          log(`Query errored: {queryName}`, vars, error);
        }

        this._dispatchErrored(queryName, vars, getErrorMsg(error));
      });

    return result;
  }
}

export const apiBase = new ApiBase();
