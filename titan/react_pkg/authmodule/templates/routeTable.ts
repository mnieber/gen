import { RouteTable } from '/src/routes/utils/RouteTable';

export const getRouteTable = () => {
  const routeTable = new RouteTable();
  routeTable.addRoutes(routes);
  return routeTable;
};

export const routes = {
  signIn: () => '/auth/sign-in/',
  signInByMagicLink: () => '/auth/sign-in/:magicLinkToken/',
  signUp: () => '/auth/sign-up/',
  termsAndConditions: () => '/terms-and-conditions/',
  requestPasswordReset: () => '/auth/request-password-reset/',
  requestMagicLink: () => '/auth/request-magic-link/',
  resetPassword: () => '/auth/reset-password/:passwordResetToken/',
  activateAccount: () => '/auth/activate-account/:activationToken/',
};

export type RoutesT = {
  signIn: () => string;
  signInByMagicLink: (params: { magicLinkToken: string }) => string;
  signUp: () => string;
  termsAndConditions: () => string;
  requestPasswordReset: () => string;
  requestMagicLink: () => string;
  resetPassword: (params: { passwordResetToken: string }) => string;
  activateAccount: (params: { activationToken: string }) => string;
};
