import { Route, Switch } from 'react-router-dom';
import { ActivateAccountPage } from '/src/auth/components/ActivateAccountPage';
import { RequestMagicLinkPage } from '/src/auth/components/RequestMagicLinkPage';
import { RequestPasswordResetPage } from '/src/auth/components/RequestPasswordResetPage';
import { ResetPasswordPage } from '/src/auth/components/ResetPasswordPage';
import { SignInPage } from '/src/auth/components/SignInPage';
import { SignUpPage } from '/src/auth/components/SignUpPage';
import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { getRouteFns } from '/src/routes/routeTable';

export const AuthSwitch = () => {
  const routes = getRouteFns<AuthRoutesT>();

  return (
    <Switch>
      <Route exact path={routes.signIn()}>
        <SignInPage />
      </Route>
      <Route exact path={routes.signInByMagicLink()}>
        <SignInPage />
      </Route>
      <Route exact path={routes.signUp()}>
        <SignUpPage />
      </Route>
      <Route exact path={routes.activateAccount()}>
        <ActivateAccountPage />
      </Route>
      <Route exact path={routes.requestPasswordReset()}>
        <RequestPasswordResetPage />
      </Route>
      <Route exact path={routes.requestMagicLink()}>
        <RequestMagicLinkPage />
      </Route>
      <Route exact path={routes.resetPassword()}>
        <ResetPasswordPage />
      </Route>
    </Switch>
  );
};
