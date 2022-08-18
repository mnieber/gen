import { RouterLink } from 'src/routes/components';
import { useRoutes } from 'src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const divTheActivationFailed = (
    <div>
      The activation failed, probably because your account is already active.{' '}
      Please try to <RouterLink to={routes.signIn()}>sign in</RouterLink> or{' '}
      <RouterLink to={routes.requestPasswordReset()}>
        reset your password
      </RouterLink>
      .
    </div>
  );

  return {
    messages: {
      divSorryThatPasswordIsTooShort: 'Sorry, that password is too short',
      divTheActivationFailed,
      divSorryTechnicalError:
        'Sorry, there seems to be a technical problem. ' +
        'Check your internet connection, or try again later.',
      pleaseProvideANewPassword: 'Please provide a new password',
      sorryThatPasswordIsTooShort: 'Sorry, that password is too short',
      divYouAreOneStepAway:
        'You are one step away from activating your account.',
      divToProceedPleaseChooseANewPassword:
        'To proceed, please choose a new password.',
    },
  };
};
