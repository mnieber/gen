import { observer } from 'mobx-react-lite';
import React from 'react';
import { useMessages } from './useMessages';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { SignUpForm } from '/src/auth/components/SignUpForm';
import { useSignUp } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { useAuthStateContext } from '/src/auth/hooks';
import { cn } from '/src/utils/classnames';

export const termsVersion: string =
  import.meta.env.VITE_TERMS_VERSION ?? '1.0.0';

export const SignUpCard = observer(() => {
  const { messages } = useMessages();
  const authState = useAuthStateContext(true);
  const signUp = useSignUp(authState).mutateAsync;

  return (
    //
    // 🔳 SignUpCard 🔳
    //
    <AuthCard id="SignUpCard">
      {
        // 🔳 Confirmation 🔳
      }
      {authState.state === States.SIGN_UP_SUCCEEDED && (
        <div>{messages.divYouHaveBeenSignedUp}</div>
      )}

      {
        // 🔳 SignUpForm 🔳
      }
      {authState.state !== States.SIGN_UP_SUCCEEDED && (
        <React.Fragment>
          <SignUpForm
            className={cn(AuthCardS.Form())}
            signUp={(email: string, acceptsTerms: boolean) => {
              return signUp({
                userId: email,
                acceptsTerms,
                termsVersionAccepted: termsVersion,
              });
            }}
            errors={authState.errors}
          />
          <div className={cn(AuthCardS.CardFooter())}>
            {messages.ifYouAlreadyHaveAnAccount}
          </div>
        </React.Fragment>
      )}
    </AuthCard>
  );
});
