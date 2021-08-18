import { observer } from 'mobx-react-lite';
import React from 'react';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { routes } from 'src/app/routeTable';
import { useAuthStateContext } from 'src/auth/components';
import { ActivateAccountForm } from 'src/auth/components/ActivateAccountForm';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { RouterLink } from 'src/widgets/components/RouterLink';

export const ActivateAccountPage: React.FC = observer(() => {
  const { authStore } = useStore();
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
    <ActivateAccountForm
      activateAccount={authStore.activateAccount}
      errors={errors}
    />
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
