export const Routes = {
  signIn: () => '/sign-in/',
  signUp: () => '/sign-up/',
  requestPasswordReset: () => '/request-password-reset/',
  resetPassword: (passwordResetToken: string) =>
    `/reset-password/${passwordResetToken}`,
  activateAccount: (activationToken: string) =>
    `/activate-account/${activationToken}`,
};
