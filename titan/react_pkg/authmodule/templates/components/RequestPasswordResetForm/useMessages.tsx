import { useRoutes } from 'src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  return {
    messages: {
      divSorryThereSeemsToBeATechnicalProblem:
        'Sorry, there seems to be a technical problem. ' +
        'Check your internet connection, or try again later.',
      divEnterYourEmailToResetYourPassword:
        'Enter your email to reset your password',
      divPleaseEnterYourEmailAddress: 'Please enter your email address',
    },
  };
};
