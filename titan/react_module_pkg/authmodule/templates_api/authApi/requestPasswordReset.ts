import { useMutation } from 'react-query';
import { States } from 'src/api/authApi/states';
import { isError } from 'src/api/authApi/utils';
import { AuthState } from 'src/auth/AuthState';
import { useAuthStore } from 'src/auth/components/useAuthStore';
import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export type ArgsT = {
  email: string;
};

export function requestPasswordReset(args: ArgsT) {
  return doQuery(
    `mutation ($email: String!) {
      requestPasswordReset(
        email: $email,
      ) {
        success,
        errors,
        passwordResetToken
      }
    }`,
    {
      email: args.email,
    }
  ).then((response: ObjT) => {
    if (isError(['requestPasswordReset', 'errors'])(response))
      return {
        success: false,
        errors: [States.REQUEST_PASSWORD_RESET_FAILED],
      };

    return {
      success: true,
      passwordResetToken: response.requestPasswordReset.passwordResetToken,
    };
  });
}

export const useRequestPasswordReset = (authState?: AuthState) => {
  const authStore = useAuthStore();
  const queryName = 'requestPasswordReset';

  return useMutation([queryName], requestPasswordReset, {
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      authStore.onRequestPasswordReset(data);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
