import { States } from 'src/api/authApi/states';
import { hasErrorCode, isError } from 'src/api/authApi/utils';
import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export async function resetPassword(
  password: string,
  passwordResetToken: string
) {
  const query = `mutation ($password: String!, $passwordResetToken: String!) {
      resetPassword(
        passwordResetToken: $passwordResetToken,
        password: $password,
      ) {
        success,
        errors,
      }
    }`;
  const response: ObjT = await doQuery(query, {
    password,
    passwordResetToken,
  });

  if (
    hasErrorCode(['resetPassword', 'errors', 'password'], 'TOO_SHORT')(response)
  )
    return {
      success: false,
      errors: [States.PASSWORD_TOO_SHORT],
    };

  if (
    hasErrorCode(
      ['resetPassword', 'errors', 'passwordResetToken'],
      'NOT_FOUND'
    )(response)
  )
    return {
      success: false,
      errors: [States.PASSWORD_RESET_TOKEN_NOT_FOUND],
    };

  if (
    hasErrorCode(
      ['resetPassword', 'errors', 'passwordResetToken'],
      'ACCOUNT_UNKNOWN'
    )(response)
  )
    return {
      success: false,
      errors: [States.PASSWORD_RESET_EMAIL_UNKNOWN],
    };

  if (isError(['resetPassword', 'errors'])(response))
    return {
      success: false,
      errors: [States.RESET_PASSWORD_FAILED],
    };

  return {
    success: true,
  };
}
