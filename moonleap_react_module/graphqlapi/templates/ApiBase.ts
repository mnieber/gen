import { Signal } from 'micro-signals';
import { LoadDataEventT } from 'src/api/events';
import { doQuery } from 'src/utils/graphqlClient';
import { erroredRS, loadingRS, updatedRS } from 'src/utils/RST';
import { ObjT } from 'src/utils/types';

export class ApiBase {
  signal: Signal<any> = new Signal();

  _dispatchUpdating(queryName: string) {
    this.signal.dispatch({
      topic: `Updating.${queryName}`,
      state: loadingRS(),
    } as LoadDataEventT);
    return Promise.resolve();
  }

  _dispatchUpdated(queryName: string, payload: any) {
    this.signal.dispatch({
      topic: `Updated.${queryName}`,
      state: updatedRS(),
      details: {
        payload,
      }
    } as LoadDataEventT);
  }

  _dispatchErrored(queryName: string, error: string) {
    this.signal.dispatch({
      topic: `Errored.${queryName}`,
      state: erroredRS(error),
    } as LoadDataEventT);
  }

  _doQuery(
    queryName: string,
    query: string,
    vars: ObjT,
    getPayload: Function,
    getErrorMsg: (error: ObjT) => string
  ) {
    return this._dispatchUpdating(queryName).then(() =>
      doQuery(query, vars)
        .then((response) => {
          this._dispatchUpdated(queryName, getPayload(response));
        })
        .catch((error) => {
          this._dispatchErrored(queryName, getErrorMsg(error));
        })
    );
  }
}
