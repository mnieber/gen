import React from 'react';
import { Route, Switch } from 'react-router-dom';
import { Routes } from 'src/app/Routes';
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
        <Route exact path={Routes.signIn()}>
          <SignInPage />
        </Route>
        <Route exact path={Routes.signUp()}>
          <SignUpPage />
        </Route>
        <Route exact path={Routes.activateAccount(':activationToken')}>
          <ActivateAccountPage />
        </Route>
        <Route exact path={Routes.requestPasswordReset()}>
          <RequestPasswordResetPage />
        </Route>
        <Route exact path={Routes.resetPassword(':passwordResetToken')}>
          <ResetPasswordPage />
        </Route>
      </Switch>
    </AuthStateProvider>
  );
};
