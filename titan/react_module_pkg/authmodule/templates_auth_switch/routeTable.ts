import { RouteTable } from 'src/utils/RouteTable';

export const routeTable = new RouteTable();

routeTable.addRoutes({
  signIn: () => '/sign-in/',
  signUp: () => '/sign-up/',
  requestPasswordReset: () => '/request-password-reset/',
  resetPassword: (passwordResetToken: string) =>
    `/reset-password/${passwordResetToken}`,
  activateAccount: (activationToken: string) =>
    `/activate-account/${activationToken}`,
});
