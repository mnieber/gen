import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { RouterLink } from '/src/routes/components';
import { getRoutes } from '/src/routes/routeTable';

export const useMessages = () => {
  const routes = getRoutes<AuthRoutesT>();

  const yourPasswordHasBeenChanged = (
    <div>
      Your password has been changed. You can now{' '}
      <RouterLink dataCy={'linkToSignIn'} to={routes.signIn()}>
        sign in
      </RouterLink>
      .
    </div>
  );

  return {
    messages: {
      yourPasswordHasBeenChanged,
    },
  };
};
