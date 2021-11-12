import * as R from 'ramda';
import { removeItemsFromArray } from 'src/utils/array';
import { ObjT } from 'src/utils/types';

// This function adds childId to its parent within parentById, and
// removes childId from any other object in parentById.
// The parent is given by parentById[parentId].
// For any object, the list of child ids is given by object[childrenIdsProp].
export function updateForeignKey(
  parentById: ObjT,
  childrenIdsProp: string,
  parentId: string,
  childId: string
) {
  const parent = parentById[parentId];
  if (parent && !parent[childrenIdsProp].includes(childId)) {
    // Remove child from existing parents
    R.forEach((parent: any) => {
      removeItemsFromArray(parent[childrenIdsProp], [childId]);
    }, R.values(parentById));

    // Add child to new parent
    parent[childrenIdsProp].push(childId);
  }
}
