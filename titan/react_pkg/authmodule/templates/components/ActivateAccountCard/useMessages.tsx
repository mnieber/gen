import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

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
