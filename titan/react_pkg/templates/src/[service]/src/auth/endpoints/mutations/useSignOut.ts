import { useObservableMutation } from '/src/api/ObservableMutation';
import { setToken } from '/src/api/graphqlClient';
import { AuthState } from '/src/auth/AuthState';
import { invalidateLoadUserId } from '/src/auth/endpoints';
import { ObjT } from '/src/utils/types';

export type ArgsT = {};

export function signOut(args: ArgsT) {
  return Promise.resolve().then(() => {
    setToken('', '');
    return {
      errors: [],
    };
  });
}

export const useSignOut = (authState?: AuthState) => {
  const queryName = 'signOut';

  return useObservableMutation({
    mutationFn: signOut,
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
