import { SelectionParamsT } from 'skandha-facets/Selection';

export const createOnSelectItemHandler =
  <ItemT extends { id: string }>(
    items: ItemT[],
    updateUrl?: (item: ItemT) => void
  ) =>
  (selectionParams: SelectionParamsT) => {
    if (
      selectionParams.itemId &&
      !(selectionParams.isCtrl || selectionParams.isShift)
    ) {
      const ufn = _getUpdateUrlFn(items, updateUrl);
      ufn && ufn(selectionParams.itemId);
    }
  };

export const _getUpdateUrlFn = <ItemT extends { id: string }>(
  items: ItemT[],
  updateUrl?: (item: ItemT) => void
) => {
  return updateUrl
    ? (itemId: string) => {
        const item = items.find((x: ItemT) => x.id === itemId);
        item && updateUrl(item);
      }
    : undefined;
};
