import { useMutation } from 'react-query';
import { AuthState } from 'src/auth/AuthState';
import { useAuthStore } from 'src/auth/components/useAuthStore';
import { setToken } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export type ArgsT = {};

export function signOut(args: ArgsT) {
  return Promise.resolve().then(() => {
    setToken('');
    return {
      errors: {},
    };
  });
}

export const useSignOut = (authState?: AuthState) => {
  const authStore = useAuthStore();
  const queryName = 'signOut';

  return useMutation([queryName], signOut, {
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      authStore.onSignOut(data);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
