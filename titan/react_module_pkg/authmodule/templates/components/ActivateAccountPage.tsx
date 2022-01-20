import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { useActivateAccount } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { ActivateAccountForm } from 'src/auth/components/ActivateAccountForm';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/routes/components';
import { routes } from 'src/routes/routes';
import { ObjT } from 'src/utils/types';

export const ActivateAccountPage: React.FC = observer(() => {
  const params = useParams() as ObjT;
  const authState = useAuthStateContext(true);
  const activateAccount = useActivateAccount(authState).mutateAsync;

  const confirmationDiv = (
    <div>
      Your account was activated. You can now{' '}
      <RouterLink dataCy={'goToSignInLink'} to={routes.signIn()}>
        sign in
      </RouterLink>
      .
    </div>
  );

  const activateAccountForm = (
    <ActivateAccountForm
      activateAccount={(password: string) =>
        activateAccount({ password, activationToken: params.activationToken })
      }
      errors={authState.errors}
    />
  );

  return (
    <AuthFrame header="Activate your account">
      <div id="ActivateAccountPage" className="">
        {authState.state === States.ACTIVATE_ACCOUNT_SUCCEEDED &&
          confirmationDiv}
        {authState.state !== States.ACTIVATE_ACCOUNT_SUCCEEDED &&
          activateAccountForm}
      </div>
    </AuthFrame>
  );
});
