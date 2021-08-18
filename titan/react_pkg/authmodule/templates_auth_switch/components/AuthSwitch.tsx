import React from 'react';
import { Route, Switch } from 'react-router-dom';
import { routes } from 'src/app/routeTable';
import { ActivateAccountPage } from 'src/auth/components/ActivateAccountPage';
import { AuthStateProvider } from 'src/auth/components/AuthStateProvider';
import { RequestPasswordResetPage } from 'src/auth/components/RequestPasswordResetPage';
import { ResetPasswordPage } from 'src/auth/components/ResetPasswordPage';
import { SignInPage } from 'src/auth/components/SignInPage';
import { SignUpPage } from 'src/auth/components/SignUpPage';

export const AuthSwitch: React.FC = () => {
  return (
    <AuthStateProvider>
      <Switch>
        <Route exact path={routes.signIn()}>
          <SignInPage />
        </Route>
        <Route exact path={routes.signUp()}>
          <SignUpPage />
        </Route>
        <Route exact path={routes.activateAccount(':activationToken')}>
          <ActivateAccountPage />
        </Route>
        <Route exact path={routes.requestPasswordReset()}>
          <RequestPasswordResetPage />
        </Route>
        <Route exact path={routes.resetPassword(':passwordResetToken')}>
          <ResetPasswordPage />
        </Route>
      </Switch>
    </AuthStateProvider>
  );
};
