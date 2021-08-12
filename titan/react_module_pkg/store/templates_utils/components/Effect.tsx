import { observer } from "mobx-react-lite";
import { merge } from "ramda";
import React from "react";
import { useParams } from "react-router-dom";
import { ObjT } from "src/utils/types";
import { useSearchParams } from "src/utils/useSearchParams";
import useDeepCompareEffect from "use-deep-compare-effect";

interface IProps<ArgsT> {
  f: (args: ArgsT) => void | (() => void);
  getArgs: (args: ObjT) => ArgsT;
}

export const Effect: <ArgsT>(props: IProps<ArgsT>) => React.ReactElement =
  observer(({ f, getArgs }) => {
    const params = useParams();
    const { all: searchParams } = useSearchParams();
    const args = getArgs(merge(params, searchParams));

    useDeepCompareEffect(() => {
      const cleanUpFunction = f(args);
      return cleanUpFunction;
    }, [f, args]);
    return <React.Fragment />;
  });

type EffectWithoutArgsPropsT = {
  f: () => void;
};

export const EffectWithoutArgs: (
  props: EffectWithoutArgsPropsT
) => React.ReactElement = observer(({ f }) => {
  useDeepCompareEffect(() => {
    const cleanUpFunction = f();
    return cleanUpFunction;
  }, [f]);
  return <React.Fragment />;
});
