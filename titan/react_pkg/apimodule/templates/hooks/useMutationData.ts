import { runInAction } from 'mobx';
import React from 'react';
import { MutationData } from 'src/api/MutationData';
import { ObjT } from 'src/utils/types';

export const useMutationData = (mutation: ObjT) => {
  const [mutationData] = React.useState(() => new MutationData());

  React.useEffect(() => {
    runInAction(() => {
      mutationData.mutation = mutation;
      mutationData.data = mutation.data;
      mutationData.status = mutation.status;
      mutationData.mutateAsync = mutation.mutateAsync;
    });
  }, [mutation, mutationData]);

  return mutationData;
};
