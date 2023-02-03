import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignInForm } from 'src/auth/components/SignInForm';
import {
  useRequestMagicLink,
  useSignIn,
  useSignInByMagicLink,
} from 'src/auth/endpoints';
import { States } from 'src/auth/endpoints/states';
import { useAuthStateContext } from 'src/auth/hooks';
import { getHomeRoute } from 'src/routes';
import { getNextUrl, useNextUrl } from 'src/utils/hooks';
import { ObjT } from 'src/utils/types';
import { useMessages } from './useMessages';

export const SignInPage = observer(() => {
  const { messages } = useMessages();

  const params = useParams() as ObjT;
  const authState = useAuthStateContext(true);
  const requestMagicLink = useRequestMagicLink(authState).mutateAsync;
  const signInByMagicLink = useSignInByMagicLink(authState).mutateAsync;
  const signIn = useSignIn(authState).mutateAsync;

  // Change the url if sign in was successfull
  useNextUrl(
    authState.state === States.SIGN_IN_SUCCEEDED ||
      authState.state === States.SIGN_IN_BY_MAGIC_LINK_SUCCEEDED
      ? getNextUrl(getHomeRoute())
      : undefined
  );

  React.useEffect(() => {
    if (params.magicLinkToken) {
      signInByMagicLink({ magicLinkToken: params.magicLinkToken });
    }
  }, [params.magicLinkToken, signInByMagicLink]);

  return (
    <AuthFrame header="Sign in" id="SignInPage">
      {authState.state === States.REQUEST_MAGIC_LINK_SUCCEEDED && (
        <div>{messages.divAMagicLinkHasBeenSentToYourEmailAddress}</div>
      )}
      <SignInForm
        signIn={(email, password) => {
          return signIn({ userId: email, password });
        }}
        requestMagicLink={(email) => {
          return requestMagicLink({ userId: email });
        }}
        errors={authState.errors}
        className="mb-4"
      />
      <div className="SignInPage__Footer flex flex-col items-center">
        {messages.divForgotYourPassword}
        <div className="flex flex-row">
          {messages.divDontHaveAnAccount}
          {messages.linkSignUp}
        </div>
      </div>
    </AuthFrame>
  );
});
