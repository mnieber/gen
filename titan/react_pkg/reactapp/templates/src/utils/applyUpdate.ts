import * as R from 'ramda';
import { ObjT } from 'src/utils/types';

export const applyUpdate = (path: string, data: ObjT, update: Function) => {
  const pathParts = path.split('.');
  applyUpdateImp(pathParts, 0, data, update);
  return data;
};

const applyUpdateImp = (
  paths: string[],
  pathIdx: number,
  data: ObjT,
  update: Function
) => {
  if (pathIdx === paths.length) {
    update(data);
  }

  const path = paths[pathIdx];
  if (path === '*') {
    const updateItem = (item: any) => {
      applyUpdateImp(paths, pathIdx + 1, item, update);
    };

    R.forEach(updateItem, Array.isArray(data) ? data : R.values(data));
  } else if (path) {
    applyUpdateImp(paths, pathIdx + 1, data[path], update);
  }
};
