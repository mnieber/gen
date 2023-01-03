import { RouterLink } from 'src/routes/components';

export const useMessages = () => {
  const divForgotYourPassword = (
    <RouterLink to="/request-password-reset/">Forgot password?</RouterLink>
  );

  const linkSignUp = <RouterLink to="/sign-up/">{'Sign Up'}</RouterLink>;

  return {
    messages: {
      divAMagicLinkHasBeenSentToYourEmailAddress:
        'A magic link has been sent to your email address.',
      divForgotYourPassword,
      divDontHaveAnAccount: <div className="mr-2">Don't have an account?</div>,
      linkSignUp,
    },
  };
};
