import { observer } from 'mobx-react-lite';
import React from 'react';
import { signUp } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { termsVersion } from 'src/auth/AuthStore';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignUpForm } from 'src/auth/components/SignUpForm';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/utils/components';

export const SignUpPage: React.FC = observer(() => {
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
            <SignUpForm
              signUp={(email: string, acceptsTerms: boolean) =>
                signUp(email, acceptsTerms, termsVersion)
              }
              errors={errors}
            />
            {alreadyHaveAnAccountDiv}
          </React.Fragment>
        )}
      </div>
    </AuthFrame>
  );
});
