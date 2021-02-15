import React from 'react';
import { Router, Switch, Route } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { createBrowserHistory } from 'history';

type PropsT = {};

export const history = createBrowserHistory();

export const UrlRouter: React.FC<PropsT> = observer((props: PropsT) => {
  return (
    <Router history={history}>
      <Switch>
      </Switch>
    </Router>
  );
});
