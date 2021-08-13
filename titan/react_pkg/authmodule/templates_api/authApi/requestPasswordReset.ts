import { States } from 'src/api/authApi/states';
import { isError } from 'src/api/authApi/utils';
import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export async function requestPasswordReset(email: string) {
  const query = `mutation ($email: String!) {
      requestPasswordReset(
        email: $email,
      ) {
        success,
        errors,
        passwordResetToken
      }
    }`;
  const response: ObjT = await doQuery(query, {
    email,
  });

  if (isError(['requestPasswordReset', 'errors'])(response))
    return {
      success: false,
      errors: [States.REQUEST_PASSWORD_RESET_FAILED],
    };

  return {
    success: true,
    passwordResetToken: response.requestPasswordReset.passwordResetToken,
  };
}
