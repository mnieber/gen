import React from 'react';
import { Route, Switch } from 'react-router-dom';
import { ActivateAccountPage } from 'src/auth/components/ActivateAccountPage';
import { AuthStateProvider } from 'src/auth/components/AuthStateProvider';
import { RequestPasswordResetPage } from 'src/auth/components/RequestPasswordResetPage';
import { ResetPasswordPage } from 'src/auth/components/ResetPasswordPage';
import { SignInPage } from 'src/auth/components/SignInPage';
import { SignUpPage } from 'src/auth/components/SignUpPage';
import { useRoutes } from 'src/routes/hooks/useRoutes';

export const AuthSwitch = () => {
  const routes = useRoutes();

  return (
    <AuthStateProvider>
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
        <Route exact path={routes.resetPassword()}>
          <ResetPasswordPage />
        </Route>
      </Switch>
    </AuthStateProvider>
  );
};
