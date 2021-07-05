import { Api } from 'src/api/Api';
import { LoadDataEventT } from 'src/api/events';

export const storeConnectsToApi = (store: any, api: Api) => {
  api.signal.add((event: LoadDataEventT) => {
    const [, queryName] = event.topic.split('.');
    store.onLoadData(event, event.payload.state, queryName);
  });
};
