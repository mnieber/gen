import { useMutation } from '@tanstack/react-query';
import { doQuery } from 'src/api/graphqlClient';
import { States } from 'src/auth/api/states';
import { hasErrorCode, isError } from 'src/auth/api/utils';
import { AuthState } from 'src/auth/AuthState';
import { ObjT } from 'src/utils/types';

export type ArgsT = {
  password: string;
  passwordResetToken: string;
};

export function resetPassword(args: ArgsT) {
  return doQuery(
    `mutation ($password: String!, $passwordResetToken: String!) {
      resetPassword(
        passwordResetToken: $passwordResetToken,
        password: $password,
      ) {
        success,
        errors,
      }
    }`,
    {
      password: args.password,
      passwordResetToken: args.passwordResetToken,
    }
  ).then((response: ObjT) => {
    if (
      hasErrorCode(
        ['resetPassword', 'errors', 'password'],
        'TOO_SHORT'
      )(response)
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
  });
}

export const useResetPassword = (authState?: AuthState) => {
  const queryName = 'resetPassword';

  return useMutation([queryName], resetPassword, {
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
