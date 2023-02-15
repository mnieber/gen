import { runInAction } from 'mobx';
import React from 'react';
import { MutationData } from 'src/api/MutationData';
import { ObjT } from 'src/utils/types';

export type OptionsT = {
  fetchAsLoad?: boolean;
};

export const useMutationData = (mutation: ObjT, options?: OptionsT) => {
  const [mutationData] = React.useState(() => new MutationData());
  const fetchAsLoad = options?.fetchAsLoad;

  React.useEffect(() => {
    runInAction(() => {
      mutationData.mutation = mutation;
      mutationData.data = mutation.data;
      mutationData.mutateAsync = mutation.mutateAsync;
      mutationData.status =
        fetchAsLoad && mutation.isFetching ? 'loading' : mutation.status;
    });
  }, [mutation, mutationData, fetchAsLoad]);

  return mutationData;
};
