import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const divSorryWeCouldNotResetThePassword = (
    <div>
      Sorry, we could not reset the password. You may try to{' '}
      <RouterLink key="_tryAgain" to={routes.requestPasswordReset()}>
        reset your password
      </RouterLink>{' '}
      again.
    </div>
  );

  return {
    messages: {
      divSorryWeCouldNotResetThePassword,
      sorryThatPasswordIsTooShort: 'Sorry, that password is too short',
      sorryWeCouldNotFindYourAccount:
        "Sorry, we could not find your account. Don't worry, this could be a technical " +
        'failure on our side. Please contact support.',
      divSorryThereSeemsToBeATechnicalProblem:
        'Sorry, there seems to be a technical problem. ' +
        'Check your internet connection, or try again later.',
      divPleaseProvideANewPassword: 'Please provide a new password',
      divEnterYourNewPassword: 'Please enter your new password',
    },
  };
};
