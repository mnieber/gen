import { RouteTable } from 'src/routes/RouteTable';

export const routeTable = new RouteTable();

routeTable.addRoutes({
  signIn: '/sign-in/',
  signUp: '/sign-up/',
  requestPasswordReset: '/request-password-reset/',
  resetPassword: `/reset-password/:passwordResetToken`,
  activateAccount: `/activate-account/:activationToken`,
});
