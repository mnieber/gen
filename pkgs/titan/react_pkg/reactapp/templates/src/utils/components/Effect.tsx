import { observer } from 'mobx-react-lite';
import { useSearchAndUrlParams } from 'src/utils/hooks/useSearchAndUrlParams';
import { ObjT } from 'src/utils/types';
import useDeepCompareEffect from 'use-deep-compare-effect';

interface IProps<ArgsT> {
  f: (args: ArgsT) => void | (() => void);
  getArgs: (args: ObjT) => ArgsT;
}

export const Effect: <ArgsT>(props: IProps<ArgsT>) => null = observer(
  ({ f, getArgs }) => {
    const args = getArgs(useSearchAndUrlParams());

    useDeepCompareEffect(() => {
      const cleanUpFunction = f(args);
      return cleanUpFunction;
    }, [f, args]);

    return null;
  }
);
