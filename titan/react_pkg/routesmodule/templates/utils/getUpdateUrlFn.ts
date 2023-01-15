export const getUpdateUrlFn = <ItemT extends { id: string }>(
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
