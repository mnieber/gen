// Import styles. This needs to be done before importing any components.
import '/src/frames/styles/index.css';
import '/src/frames/styles/index.scss';

import { toJS } from 'mobx';
import { applyFormatters } from 'mobx-log';
import { setOptions as setResourceStatesOptions } from 'mobx-resource-states';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { setOptions as setNavHandlerOptions } from 'react-nav-handler';
import { matchPath, useRouteMatch } from 'react-router-dom';
import { setOptions as setSkandhaOptions } from 'skandha';
import { App } from '/src/app/components';
import { flags } from '/src/app/flags';
import { log } from '/src/utils/logging';

const strict = false;

if (import.meta.env.DEV) {
  applyFormatters();
}

setSkandhaOptions({
  logging: flags.logSkandha,
  formatObject: toJS,
});

setNavHandlerOptions({
  useRouteMatch: useRouteMatch,
  matchPath: matchPath,
});

setResourceStatesOptions({
  logging: flags.logResourceStates,
  log: log,
});

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const body = <App />;

root.render(strict ? <React.StrictMode>{body}</React.StrictMode> : body);
