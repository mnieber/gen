import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

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
