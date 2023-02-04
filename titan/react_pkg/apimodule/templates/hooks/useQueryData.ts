import { runInAction } from 'mobx';
import React from 'react';
import { QueryData } from 'src/api/QueryData';
import { ObjT } from 'src/utils/types';

export const useQueryData = (query: ObjT) => {
  const [queryData] = React.useState(() => new QueryData());

  React.useEffect(() => {
    runInAction(() => {
      queryData.query = query;
      queryData.data = query.data;
      queryData.status = query.status;
    });
  }, [query, queryData]);

  return queryData;
};
