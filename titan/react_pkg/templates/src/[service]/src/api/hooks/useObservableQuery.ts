import { runInAction } from 'mobx';
import React from 'react';
import { ObservableQuery, QueryDataT } from '/src/api/ObservableQuery';
import { flags } from '/src/app/flags';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export interface TanstackQuery {
  data: QueryDataT;
  status: string;
  isFetching: boolean;
}

export type OptionsT = {
  fetchAsLoad?: boolean;
  debugLabel?: string;
};

export const useObservableQuery = (
  query: TanstackQuery,
  options?: OptionsT
) => {
  const fetchAsLoad = options?.fetchAsLoad;
  const debugLabel = options?.debugLabel;

  const observableQuery = useBuilder(() => {
    const observableQuery = new ObservableQuery();
    observableQuery.debugLabel = debugLabel;
    updateObservableQuery(observableQuery, query, fetchAsLoad);
    return observableQuery;
  });

  React.useEffect(() => {
    runInAction(() => {
      updateObservableQuery(observableQuery, query, fetchAsLoad);
      if (debugLabel && flags.logQueries) {
        observableQuery.log(
          `ObservableQuery ${observableQuery.id} (${debugLabel}) ` +
            `updated to ${observableQuery.status}`
        );
      }
    });
  }, [query]);

  return observableQuery;
};

const updateObservableQuery = (
  observableQuery: ObservableQuery,
  tanstackQuery: TanstackQuery,
  fetchAsLoad: boolean | undefined
) => {
  observableQuery.data = tanstackQuery.data;
  observableQuery.status =
    fetchAsLoad && tanstackQuery.isFetching ? 'loading' : tanstackQuery.status;
};
