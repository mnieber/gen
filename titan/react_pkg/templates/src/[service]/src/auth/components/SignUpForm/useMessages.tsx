import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { RouterLink } from '/src/routes/components';
import { getRouteFns } from '/src/routes/routeTable';

export const useMessages = () => {
  const routes = getRouteFns<AuthRoutesT>();

  const divIAgreeToTheTerms = (
    <label htmlFor={'acceptsTerms'}>
      I agree to the{' '}
      <RouterLink key="termsAndConditions" to={routes.termsAndConditions()}>
        Terms and Conditions
      </RouterLink>
    </label>
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
