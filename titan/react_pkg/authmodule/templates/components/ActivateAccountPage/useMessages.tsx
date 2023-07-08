import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const yourAccountWasActivated = (
    <div>
      Your account was activated. You can now{' '}
      <RouterLink dataCy={'goToSignInLink'} to={routes.signIn()}>
        sign in
      </RouterLink>
      .
    </div>
  );

  return {
    messages: {
      yourAccountWasActivated,
    },
  };
};
