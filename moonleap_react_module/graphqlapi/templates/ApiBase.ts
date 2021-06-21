import { Signal } from 'micro-signals';
import { ObjT } from 'src/utils/types';
import { doQuery } from 'src/utils/graphqlClient';
import { EventT } from 'src/utils/events';
import { erroredRS, loadingRS, updatedRS } from 'src/utils/RST';

export class ApiBase {
  signal: Signal<any> = new Signal();

  _dispatchLoading(queryName: string) {
    this.signal.dispatch({
      topic: `Loading.${queryName}`,
      state: loadingRS(),
    } as EventT);
    return Promise.resolve();
  }

  _dispatchPayload(queryName: string, payload: any) {
    this.signal.dispatch({
      topic: `Loading.${queryName}`,
      state: updatedRS(),
      payload,
    } as EventT);
  }

  _dispatchError(queryName: string, error: string) {
    this.signal.dispatch({
      topic: `Errored.${queryName}`,
      state: erroredRS(error),
    } as EventT);
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
