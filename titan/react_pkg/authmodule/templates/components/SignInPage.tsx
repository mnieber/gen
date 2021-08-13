import { observer } from 'mobx-react-lite';
import React from 'react';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { useAuthStateContext } from 'src/auth/components';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignInForm } from 'src/auth/components/SignInForm';
import { getNextUrl } from 'src/utils/urlParams';
import { useNextUrl } from 'src/utils/useNextUrl';
import { RouterLink } from 'src/widgets/components/RouterLink';

export const SignInPage: React.FC = observer(() => {
  const { authStore } = useStore();
  const { state, errors } = useAuthStateContext(true);

  // Change the url if sign in was successfull
  useNextUrl(
    state === States.SIGN_IN_SUCCEEDED ? getNextUrl('/home') : undefined
  );

  return (
    <AuthFrame header="Sign in">
      <div id="SignInPage" className="">
        <SignInForm
          signIn={(email, password) => {
            authStore.signIn(email, password);
          }}
          errors={errors}
        />
        <RouterLink to="/request-password-reset/">Forgot password?</RouterLink>
        <RouterLink to="/sign-up/">
          {"Don't have an account? Sign Up"}
        </RouterLink>
      </div>
    </AuthFrame>
  );
});
