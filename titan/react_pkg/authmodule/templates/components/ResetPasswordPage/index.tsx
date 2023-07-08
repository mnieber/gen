import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { useMessages } from './useMessages';
import { AuthFrame } from '/src/auth/components/AuthFrame';
import { ResetPasswordForm } from '/src/auth/components/ResetPasswordForm';
import { useResetPassword } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { useAuthStateContext } from '/src/auth/hooks';

export const ResetPasswordPage = observer(() => {
  const { messages } = useMessages();
  const params = useParams();
  const authState = useAuthStateContext(true);
  const resetPassword = useResetPassword(authState).mutateAsync;

  const isPasswordChanged = authState.state === States.RESET_PASSWORD_SUCCEEDED;

  return (
    <AuthFrame header="Change your password" id="ResetPasswordPage">
      {isPasswordChanged && <div>{messages.yourPasswordHasBeenChanged}</div>}
      {!isPasswordChanged && (
        <ResetPasswordForm
          errors={authState.errors}
          resetPassword={(password) => {
            return resetPassword({
              password,
              passwordResetToken: (params as any).passwordResetToken,
            });
          }}
        />
      )}
    </AuthFrame>
  );
});
