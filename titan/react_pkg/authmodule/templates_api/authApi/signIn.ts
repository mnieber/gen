import { States } from 'src/api/authApi/states';
import { hasErrorCode, isError } from 'src/api/authApi/utils';
import { doQuery, setToken } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export async function signIn(userId: string, password: string) {
  const query = `mutation ($email: String!, $password: String!) {
      tokenAuth(
        email: $email,
        password: $password
      ) {
        success,
        errors,
        token,
        refreshToken,
      }
    }`;

  const response: ObjT = await doQuery(query, {
    email: userId,
    password,
  });

  if (
    hasErrorCode(
      ['tokenAuth', 'errors', 'nonFieldErrors'],
      'INVALID_CREDENTIALS'
    )(response)
  )
    return {
      success: false,
      errors: [States.INVALID_CREDENTIALS],
    };

  if (isError(['tokenAuth', 'errors'])(response))
    return {
      success: false,
      errors: [States.SIGN_IN_FAILED],
    };

  const token = response.tokenAuth.token;
  setToken(token);

  return {
    success: true,
    token,
    userId,
  };
}
