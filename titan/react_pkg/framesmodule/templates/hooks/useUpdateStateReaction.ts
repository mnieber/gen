import { comparer, IEqualsComparer, reaction } from 'mobx';
import React from 'react';
import { flags } from 'src/app/flags';

export type PropsT<ArgsT> = {
  getInputs: () => ArgsT;
  updateState: (args: ArgsT) => any;
  logState?: (args: ArgsT) => any;
  equals?: IEqualsComparer<ArgsT>;
};

export const useUpdateStateReaction = <ArgsT>(props: PropsT<ArgsT>) => {
  const [cleanupFunction] = React.useState(() => {
    return reaction(
      () => props.getInputs(),
      (inputs) => {
        props.updateState(inputs);
        if (flags.logStateProviders && props.logState) {
          props.logState(inputs);
        }
      },
      { fireImmediately: true, equals: props.equals ?? comparer.default }
    );
  });

  React.useEffect(() => cleanupFunction, [cleanupFunction]);
};
