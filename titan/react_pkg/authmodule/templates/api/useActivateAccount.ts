import { useMutation } from '@tanstack/react-query';
import { States } from 'src/auth/api/states';
import { hasErrorCode, isError } from 'src/auth/api/utils';
import { AuthState } from 'src/auth/AuthState';
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
  const queryName = 'activateAccount';

  return useMutation([queryName], activateAccount, {
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
