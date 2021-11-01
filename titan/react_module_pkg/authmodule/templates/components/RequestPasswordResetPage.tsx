import { observer } from 'mobx-react-lite';
import React from 'react';
import { requestPasswordReset } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { RequestPasswordResetForm } from 'src/auth/components/RequestPasswordResetForm';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/routes/components';

export const RequestPasswordResetPage: React.FC = observer(() => {
  const { errors, state } = useAuthStateContext(true);

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
            resetPassword={requestPasswordReset}
            errors={errors}
          />
        )}
        <RouterLink dataCy="goToSignInLink" to="/sign-in/">
          Sign in
        </RouterLink>
      </div>
    </AuthFrame>
  );
});
