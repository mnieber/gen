import { createBrowserHistory } from 'history';
import { createObservableHistory } from 'mobx-observable-history';
import { patchHistory } from '/src/utils/urls';

export const history = patchHistory(createBrowserHistory());
export const navigation = createObservableHistory(history);
