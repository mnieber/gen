import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { useResetPassword } from 'src/auth/api';
import { States } from 'src/auth/api/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { ResetPasswordForm } from 'src/auth/components/ResetPasswordForm';
import { useAuthStateContext } from 'src/auth/hooks';
import { useMessages } from './useMessages';

export const ResetPasswordPage: React.FC = observer(() => {
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
          resetPassword={(password) =>
            resetPassword({
              password,
              passwordResetToken: (params as any).passwordResetToken,
            })
          }
        />
      )}
    </AuthFrame>
  );
});
