import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { resetPassword } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { ResetPasswordForm } from 'src/auth/components/ResetPasswordForm';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/routes/components';

export const ResetPasswordPage: React.FC = observer(() => {
  const params = useParams();
  const { errors, state } = useAuthStateContext(true);

  const explanationDiv = <div>Please enter your new password.</div>;
  const confirmationDiv = (
    <div>
      Your password has been changed. You can now{' '}
      <RouterLink dataCy={'goToSignInLink'} to={'/sign-in/'}>
        sign in
      </RouterLink>
    </div>
  );

  const isPasswordChanged = state === States.RESET_PASSWORD_SUCCEEDED;

  return (
    <AuthFrame header="Change your password">
      <div id="ResetPasswordPage" className="">
        {isPasswordChanged && confirmationDiv}
        {!isPasswordChanged && explanationDiv}
        {!isPasswordChanged && (
          <ResetPasswordForm
            errors={errors}
            resetPassword={(password) =>
              resetPassword(password, (params as any).passwordResetToken)
            }
          />
        )}
      </div>
    </AuthFrame>
  );
});
