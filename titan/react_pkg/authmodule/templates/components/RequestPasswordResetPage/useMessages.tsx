import { RouterLink } from 'src/routes/components';
import { useRoutes } from 'src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const haveYouFoundYourPassword = (
    <div>
      If you've found your password then you can{' '}
      <RouterLink
        key="_signIn"
        dataCy="goToSignInLink"
        to={routes.signIn()}
        className="ml-1"
      >
        sign in
      </RouterLink>
      .
    </div>
  );

  return {
    messages: {
      haveYouFoundYourPassword,
      divYourPasswordHasBeenReset:
        'Your password has been reset. Please check your email for further instructions.',
    },
  };
};
