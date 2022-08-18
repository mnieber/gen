import { RouterLink } from 'src/routes/components';
import { useRoutes } from 'src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const divForgotYourPassword = (
    <RouterLink to="/request-password-reset/">Forgot password?</RouterLink>
  );

  const linkSignUp = (
    <RouterLink to="/sign-up/">{"Don't have an account? Sign Up"}</RouterLink>
  );

  return {
    messages: {
      divAMagicLinkHasBeenSentToYourEmailAddress:
        'A magic link has been sent to your email address.',
      divForgotYourPassword,
      divDontHaveAnAccount: "Don't have an account?",
      linkSignUp,
    },
  };
};
