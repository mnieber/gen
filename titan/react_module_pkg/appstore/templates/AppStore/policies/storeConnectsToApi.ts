import { apiBase } from 'src/api/ApiBase';
import { LoadDataEventT } from 'src/api/events';

export const storeConnectsToApi = (store: any) => {
  if (store.onLoadData) {
    apiBase.signal.add((event: LoadDataEventT) => {
      const [, queryName] = event.topic.split('.');
      store.onLoadData(
        event.payload.state,
        queryName,
        event.payload.vars,
        event.payload.data,
        event
      );
    });
  }
};
