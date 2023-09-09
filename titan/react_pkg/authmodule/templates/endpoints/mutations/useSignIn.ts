import { useObservableMutation } from '/src/api/ObservableMutation';
import { doQuery, setToken } from '/src/api/graphqlClient';
import { AuthState } from '/src/auth/AuthState';
import { invalidateLoadUserId } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { hasErrorCode, isError } from '/src/auth/endpoints/utils';
import { ObjT } from '/src/utils/types';

export type ArgsT = {
  userId: string;
  password: string;
};

export function signIn(args: ArgsT) {
  return doQuery(
    `mutation ($email: String!, $password: String!) {
      signIn(
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
        ['signIn', 'errors', 'nonFieldErrors'],
        'INVALID_CREDENTIALS'
      )(response)
    )
      return {
        success: false,
        errors: [States.INVALID_CREDENTIALS],
      };

    if (isError(['signIn', 'errors'])(response))
      return {
        success: false,
        errors: [States.SIGN_IN_FAILED],
      };

    const token = response.signIn.token;
    const refreshToken = response.signIn.refreshToken;
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

  return useObservableMutation({
    mutationFn: signIn,
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      invalidateLoadUserId({});
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
