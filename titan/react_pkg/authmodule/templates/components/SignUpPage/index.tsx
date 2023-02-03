import { observer } from 'mobx-react-lite';
import React from 'react';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignUpForm } from 'src/auth/components/SignUpForm';
import { useSignUp } from 'src/auth/endpoints';
import { States } from 'src/auth/endpoints/states';
import { useAuthStateContext } from 'src/auth/hooks';
import { useMessages } from './useMessages';

export const termsVersion: string =
  process.env.REACT_APP_TERMS_VERSION ?? '1.0.0';

export const SignUpPage = observer(() => {
  const { messages } = useMessages();
  const authState = useAuthStateContext(true);
  const signUp = useSignUp(authState).mutateAsync;

  return (
    <AuthFrame header="Sign Up" id="SignUpPage">
      {authState.state === States.SIGN_UP_SUCCEEDED && (
        <div>{messages.divYouHaveBeenSignedUp}</div>
      )}
      {authState.state !== States.SIGN_UP_SUCCEEDED && (
        <React.Fragment>
          <SignUpForm
            signUp={(email: string, acceptsTerms: boolean) => {
              return signUp({
                userId: email,
                acceptsTerms,
                termsVersionAccepted: termsVersion,
              });
            }}
            errors={authState.errors}
          />
          <div className="mt-4">{messages.ifYouAlreadyHaveAnAccount}</div>
        </React.Fragment>
      )}
    </AuthFrame>
  );
});
