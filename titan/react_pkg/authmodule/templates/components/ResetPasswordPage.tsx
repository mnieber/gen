import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { useAuthStateContext } from 'src/auth/components';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { ResetPasswordForm } from 'src/auth/components/ResetPasswordForm';
import { RouterLink } from 'src/widgets/components/RouterLink';

export const ResetPasswordPage: React.FC = observer(() => {
  const { authStore } = useStore();
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
              authStore.resetPassword(
                password,
                (params as any).passwordResetToken
              )
            }
          />
        )}
      </div>
    </AuthFrame>
  );
});
