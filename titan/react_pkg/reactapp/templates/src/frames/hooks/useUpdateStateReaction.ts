import { reaction } from 'mobx';
import React from 'react';

export type PropsT<ArgsT> = {
  getInputs: () => ArgsT;
  updateState: (args: ArgsT) => any;
  destroyState?: () => any;
};

export const useUpdateStateReaction = <ArgsT>(props: PropsT<ArgsT>) => {
  return React.useEffect(() => {
    const cleanUpReaction = reaction(
      () => props.getInputs(),
      (inputs) => props.updateState(inputs),
      { fireImmediately: true }
    );
    return () => {
      cleanUpReaction();
      if (props.destroyState) {
        props.destroyState();
      }
    };
  });
};
