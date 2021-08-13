import { observer } from 'mobx-react-lite';
import React from 'react';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { useAuthStateContext } from 'src/auth/components';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignUpForm } from 'src/auth/components/SignUpForm';
import { RouterLink } from 'src/widgets/components/RouterLink';

export const SignUpPage: React.FC = observer(() => {
  const { authStore } = useStore();
  const { errors, state } = useAuthStateContext(true);

  const confirmationDiv = (
    <div>
      You have been signed up. Please check your email for further instructions.
    </div>
  );

  const alreadyHaveAnAccountDiv = (
    <div className="mt-4">
      If you already have an account then you can{' '}
      <RouterLink dataCy={'goToSignInLink'} className="ml-2" to={'/sign-in/'}>
        sign in
      </RouterLink>
    </div>
  );

  return (
    <AuthFrame header="Sign Up">
      <div id="SignUpPage">
        {state === States.SIGN_UP_SUCCEEDED && confirmationDiv}
        {state !== States.SIGN_UP_SUCCEEDED && (
          <React.Fragment>
            <SignUpForm signUp={authStore.signUp} errors={errors} />
            {alreadyHaveAnAccountDiv}
          </React.Fragment>
        )}
      </div>
    </AuthFrame>
  );
});
