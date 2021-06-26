import { Signal } from 'micro-signals';
import { LoadDataEventT } from 'src/api/events';
import { doQuery } from 'src/utils/graphqlClient';
import { erroredRS, loadingRS, updatedRS } from 'src/utils/RST';
import { ObjT } from 'src/utils/types';

export class ApiBase {
  signal: Signal<any> = new Signal();

  _dispatchLoading(queryName: string) {
    this.signal.dispatch({
      topic: `Loading.${queryName}`,
      state: loadingRS(),
    } as LoadDataEventT);
    return Promise.resolve();
  }

  _dispatchPayload(queryName: string, payload: any) {
    this.signal.dispatch({
      topic: `Loading.${queryName}`,
      state: updatedRS(),
      payload,
    } as LoadDataEventT);
  }

  _dispatchError(queryName: string, error: string) {
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
    return this._dispatchLoading(queryName).then(() =>
      doQuery(query, vars)
        .then((response) => {
          this._dispatchPayload(queryName, getPayload(response));
        })
        .catch((error) => {
          this._dispatchError(queryName, getErrorMsg(error));
        })
    );
  }
}
