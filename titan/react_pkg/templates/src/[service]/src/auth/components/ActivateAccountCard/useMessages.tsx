import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { RouterLink } from '/src/routes/components';
import { getRouteFns } from '/src/routes/routeTable';

export const useMessages = () => {
  const routes = getRouteFns<AuthRoutesT>();

  const yourAccountWasActivated = (
    <div>
      Your account was activated. You can now{' '}
      <RouterLink dataCy={'linkToSignIn'} to={routes.signIn()}>
        sign in
      </RouterLink>
      .
    </div>
  );

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
      yourAccountWasActivated,
    },
  };
};
