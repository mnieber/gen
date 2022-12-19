import React from 'react';

export const useRingIdx = (length: number, initialValue?: number) => {
  const [idx, setIdx] = React.useState(initialValue ?? 0);

  const decIdx = React.useCallback(() => {
    setIdx(idx > 0 ? idx - 1 : length - 1);
  }, [idx, setIdx, length]);

  const incIdx = React.useCallback(() => {
    setIdx(idx < length - 1 ? idx + 1 : 0);
  }, [idx, setIdx, length]);

  return {
    idx,
    setIdx,
    decIdx,
    incIdx,
    length,
  };
};
