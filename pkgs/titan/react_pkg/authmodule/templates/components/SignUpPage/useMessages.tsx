import { RouterLink } from 'src/routes/components';
import { useRoutes } from 'src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const ifYouAlreadyHaveAnAccount = (
    <div>
      If you already have an account then you can{' '}
      <RouterLink
        key="_signIn"
        dataCy={'goToSignInLink'}
        className=""
        to={routes.signIn()}
      >
        sign in
      </RouterLink>
    </div>
  );

  return {
    messages: {
      ifYouAlreadyHaveAnAccount,
      divYouHaveBeenSignedUp:
        'You have been signed up. Please check your email for further instructions.',
    },
  };
};
