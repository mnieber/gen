import React from 'react';
import { observer } from 'mobx-react-lite';
import useDeepCompareEffect from 'use-deep-compare-effect';

export const EffectWithoutArgs: (props: {
  f: () => void;
}) => React.ReactElement = observer(({ f }) => {
  useDeepCompareEffect(() => {
    const cleanUpFunction = f();
    return cleanUpFunction;
  }, [f]);
  return <React.Fragment />;
});
