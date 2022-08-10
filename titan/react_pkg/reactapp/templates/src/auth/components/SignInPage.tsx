import { observer } from 'mobx-react-lite';
import React from 'react';
import { useSignIn } from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignInForm } from 'src/auth/components/SignInForm';
import { useAuthStateContext } from 'src/auth/components/useAuthStateContext';
import { RouterLink } from 'src/routes/components';
import { getNextUrl, useNextUrl } from 'src/utils/useNextUrl';

export const SignInPage: React.FC = observer(() => {
  const authState = useAuthStateContext(true);
  const signIn = useSignIn(authState).mutateAsync;

  // Change the url if sign in was successfull
  useNextUrl(
    authState.state === States.SIGN_IN_SUCCEEDED
      ? getNextUrl('/home')
      : undefined
  );

  return (
    <AuthFrame header="Sign in">
      <div id="SignInPage" className="">
        <SignInForm
          signIn={(email, password) => {
            signIn({ userId: email, password });
          }}
          errors={authState.errors}
        />
        <RouterLink to="/request-password-reset/">Forgot password?</RouterLink>
        <RouterLink to="/sign-up/">
          {"Don't have an account? Sign Up"}
        </RouterLink>
      </div>
    </AuthFrame>
  );
});
