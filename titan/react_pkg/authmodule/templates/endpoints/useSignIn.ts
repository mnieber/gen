import { useMutation } from '@tanstack/react-query';
import { doQuery, setToken } from 'src/api/graphqlClient';
import { queryClient } from 'src/api/queryClient';
import { AuthState } from 'src/auth/AuthState';
import { States } from 'src/auth/endpoints/states';
import { hasErrorCode, isError } from 'src/auth/endpoints/utils';
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
    const refreshToken = response.tokenAuth.refreshToken;
    setToken(token, refreshToken);

    return {
      success: true,
      token,
      userId: args.userId,
    };
  });
}

export const useSignIn = (authState?: AuthState) => {
  const queryName = 'signIn';

  return useMutation({
    mutationKey: [queryName],
    mutationFn: signIn,
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      queryClient.invalidateQueries({ queryKey: ['loadUserId'] });
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
