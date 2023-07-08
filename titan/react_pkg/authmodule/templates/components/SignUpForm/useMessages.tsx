import { RouterLink } from '/src/routes/components';
import { useRoutes } from '/src/routes/hooks/useRoutes';

export const useMessages = () => {
  const routes = useRoutes();

  const divIAgreeToTheTerms = (
    <p>
      I agree to the{' '}
      <RouterLink key="termsAndConditions" to={routes.termsAndConditions()}>
        Terms and Conditions
      </RouterLink>
    </p>
  );

  return {
    messages: {
      divIAgreeToTheTerms,
      divPleaseEnterYourEmailAddress: 'Please enter your email address',
      divYouNeedToAcceptTheTermsAndConditions:
        'You need to accept the terms and conditions',
      divSorryThereSeemsToBeATechnicalProblem:
        'Sorry, there seems to be a technical problem. ' +
        'Check your internet connection, or try again later.',
    },
  };
};
