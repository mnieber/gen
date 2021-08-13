import { observer } from 'mobx-react-lite';
import React from 'react';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { useAuthStateContext } from 'src/auth/components';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { RequestPasswordResetForm } from 'src/auth/components/RequestPasswordResetForm';
import { RouterLink } from 'src/widgets/components/RouterLink';

export const RequestPasswordResetPage: React.FC = observer(() => {
  const { authStore } = useStore();

  const { state } = useAuthStateContext(true);

  const confirmationDiv = (
    <div>
      Your password has been reset. Please check your email for further
      instructions.
    </div>
  );

  return (
    <AuthFrame header="Reset your password">
      <div id="RequestPasswordResetPage" className="">
        {state === States.REQUEST_PASSWORD_RESET_SUCCEEDED && confirmationDiv}
        {state !== States.REQUEST_PASSWORD_RESET_SUCCEEDED && (
          <RequestPasswordResetForm
            resetPassword={authStore.requestPasswordReset}
          />
        )}
        <RouterLink dataCy="goToSignInLink" to="/sign-in/">
          Sign in
        </RouterLink>
      </div>
    </AuthFrame>
  );
});
