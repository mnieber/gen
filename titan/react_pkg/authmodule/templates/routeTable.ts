import { RouteTable } from '/src/routes/utils/RouteTable';

export const getRouteTable = () => {
  const routeTable = new RouteTable();

  routeTable.addRoutes({
    signIn: () => '/sign-in/',
    signInByMagicLink: () => '/sign-in/:magicLinkToken/',
    signUp: () => '/sign-up/',
    requestPasswordReset: () => '/request-password-reset/',
    resetPassword: () => '/reset-password/:passwordResetToken/',
    activateAccount: () => '/activate-account/:activationToken/',
  });

  return routeTable;
};
