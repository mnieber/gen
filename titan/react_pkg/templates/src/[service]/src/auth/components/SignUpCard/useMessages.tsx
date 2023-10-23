import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { RouterLink } from '/src/routes/components';
import { getRoutes } from '/src/routes/routeTable';

export const useMessages = () => {
  const routes = getRoutes<AuthRoutesT>();

  const ifYouAlreadyHaveAnAccount = (
    <div>
      If you already have an account then you can{' '}
      <RouterLink key="_signIn" dataCy={'navToSignInLink'} to={routes.signIn()}>
        sign in
      </RouterLink>
      .
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
