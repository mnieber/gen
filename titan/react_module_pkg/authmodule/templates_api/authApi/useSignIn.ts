import { useMutation } from 'react-query';
import { States } from 'src/api/authApi/states';
import { hasErrorCode, isError } from 'src/api/authApi/utils';
import { AuthState } from 'src/auth/AuthState';
import { doQuery, setToken } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export type ArgsT = {
  userId: string;
  password: string;
};

export function signIn(args: ArgsT) {
  return doQuery(
    `mutation ($email: String!, $password: String!) {
      tokenAuth(
        email: $email,
        password: $password
      ) {
        success,
        errors,
        token,
        refreshToken,
      }
    }`,
    {
      email: args.userId,
      password: args.password,
    }
  ).then((response: ObjT) => {
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
      userId: args.userId,
    };
  });
}

export const useSignIn = (authState?: AuthState) => {
  const queryName = 'signIn';

  return useMutation([queryName], signIn, {
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
