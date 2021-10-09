import { observer } from 'mobx-react-lite';
import React from 'react';
import { activateAccount } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { routes } from 'src/app/routeTable';
import { ActivateAccountForm } from 'src/auth/components/ActivateAccountForm';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/utils/components';

export const ActivateAccountPage: React.FC = observer(() => {
  const { errors, state } = useAuthStateContext(true);

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
    <ActivateAccountForm activateAccount={activateAccount} errors={errors} />
  );

  return (
    <AuthFrame header="Activate your account">
      <div id="ActivateAccountPage" className="">
        {state === States.ACTIVATE_ACCOUNT_SUCCEEDED && confirmationDiv}
        {state !== States.ACTIVATE_ACCOUNT_SUCCEEDED && activateAccountForm}
      </div>
    </AuthFrame>
  );
});
