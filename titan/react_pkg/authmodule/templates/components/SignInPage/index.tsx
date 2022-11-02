import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import {
  useRequestMagicLink,
  useSignIn,
  useSignInByMagicLink,
} from 'src/auth/api';
import { States } from 'src/auth/api/states';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { SignInForm } from 'src/auth/components/SignInForm';
import { useAuthStateContext } from 'src/auth/hooks';
import { useRoutes } from 'src/routes/hooks/useRoutes';
import { ObjT } from 'src/utils/types';
import { getNextUrl, useNextUrl } from 'src/utils/useNextUrl';
import { useMessages } from './useMessages';

export const SignInPage: React.FC = observer(() => {
  const { messages } = useMessages();

  const routes = useRoutes();
  const params = useParams() as ObjT;
  const authState = useAuthStateContext(true);
  const requestMagicLink = useRequestMagicLink(authState).mutateAsync;
  const signInByMagicLink = useSignInByMagicLink(authState).mutateAsync;
  const signIn = useSignIn(authState).mutateAsync;

  // Change the url if sign in was successfull
  useNextUrl(
    authState.state === States.SIGN_IN_SUCCEEDED ||
      authState.state === States.SIGN_IN_BY_MAGIC_LINK_SUCCEEDED
      ? getNextUrl(routes.searchLandingView())
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
          signIn({ userId: email, password });
        }}
        requestMagicLink={(email) => {
          requestMagicLink({ userId: email });
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
