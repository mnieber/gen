import { useObservableMutation } from '/src/api/ObservableMutation';
import { setToken } from '/src/api/graphqlClient';
import { queryClient } from '/src/api/queryClient';
import { AuthState } from '/src/auth/AuthState';
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
      // We completely clear the query cache so that the anonymous user
      // will never see results from the previous user.
      queryClient.getQueryCache().clear();
      if (authState) authState.onUpdated(queryName, data);
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
