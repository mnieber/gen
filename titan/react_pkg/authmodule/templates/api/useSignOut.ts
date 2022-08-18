import { useMutation } from '@tanstack/react-query';
import { setToken } from 'src/api/graphqlClient';
import { queryClient } from 'src/api/queryClient';
import { AuthState } from 'src/auth/AuthState';
import { ObjT } from 'src/utils/types';

export type ArgsT = {};

export function signOut(args: ArgsT) {
  return Promise.resolve().then(() => {
    setToken('', '');
    return {
      errors: {},
    };
  });
}

export const useSignOut = (authState?: AuthState) => {
  const queryName = 'signOut';

  return useMutation([queryName], signOut, {
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      queryClient.invalidateQueries(['loadUserId']);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
