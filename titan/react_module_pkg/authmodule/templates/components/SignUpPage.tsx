import { observer } from 'mobx-react-lite';
import React from 'react';
import { useSignUp } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignUpForm } from 'src/auth/components/SignUpForm';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/routes/components';

export const termsVersion: string =
  process.env.REACT_APP_TERMS_VERSION ?? '1.0.0';

export const SignUpPage: React.FC = observer(() => {
  const authState = useAuthStateContext(true);
  const signUp = useSignUp(authState).mutateAsync;

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
        {authState.state === States.SIGN_UP_SUCCEEDED && confirmationDiv}
        {authState.state !== States.SIGN_UP_SUCCEEDED && (
          <React.Fragment>
            <SignUpForm
              signUp={(email: string, acceptsTerms: boolean) =>
                signUp({
                  userId: email,
                  acceptsTerms,
                  termsVersionAccepted: termsVersion,
                })
              }
              errors={authState.errors}
            />
            {alreadyHaveAnAccountDiv}
          </React.Fragment>
        )}
      </div>
    </AuthFrame>
  );
});
