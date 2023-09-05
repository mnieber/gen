import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks';

export const useMessages = () => {
  const routes = useRoutes();

  const divForgotYourPassword = (
    <div>
      Forgot your password? You can request a{' '}
      <RouterLink to={routes.requestMagicLink()}>magic link</RouterLink> or a{' '}
      <RouterLink to={routes.requestPasswordReset()}>password reset</RouterLink>
      .
    </div>
  );

  return {
    messages: {
      divAMagicLinkHasBeenSentToYourEmailAddress:
        'A magic link has been sent to your email address.',
      divForgotYourPassword,
      createAccount: 'Create An Account',
    },
  };
};
