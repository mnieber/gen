import { useMutation } from 'react-query';
import { States } from 'src/api/authApi/states';
import { hasErrorCode, isError } from 'src/api/authApi/utils';
import { AuthState } from 'src/auth/AuthState';
import { useAuthStore } from 'src/auth/components/useAuthStore';
import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export type ArgsT = {
  activationToken: string;
  password: string;
};

export function activateAccount(args: ArgsT) {
  return doQuery(
    `mutation (
      $activationToken: String!,
      $password: String!,
    ) {
      activateAccount(
        activationToken: $activationToken,
        password: $password,
      ) {
        success,
        errors,
      }
    }`,
    {
      activationToken: args.activationToken,
      password: args.password,
    }
  ).then((response: ObjT) => {
    if (
      hasErrorCode(
        ['activateAccount', 'errors', 'password'],
        'TOO_SHORT'
      )(response)
    )
      return {
        success: false,
        errors: [States.PASSWORD_TOO_SHORT],
      };

    if (
      hasErrorCode(
        ['activateAccount', 'errors', 'activationToken'],
        'NOT_FOUND'
      )(response)
    )
      return {
        success: false,
        errors: [States.ACTIVATION_TOKEN_NOT_FOUND],
      };

    if (isError(['activateAccount', 'errors'])(response))
      return {
        success: false,
        errors: [States.ACTIVATE_ACCOUNT_FAILED],
      };

    return {
      success: true,
    };
  });
}

export const useActivateAccount = (authState?: AuthState) => {
  const authStore = useAuthStore();
  const queryName = 'activateAccount';

  return useMutation([queryName], activateAccount, {
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      authStore.onActivateAccount(data);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
