import * as R from 'ramda';
import { ObjT } from 'src/utils/types';

type PropsT = {
  storeName: string;
  queryName: string;
  data: ObjT;
  propNames: string[];
  handled: string[];
  ignored?: string[];
};

export const mustHandleQuery = (props: PropsT) => {
  const isIgnored = (props.ignored ?? []).includes(props.queryName);
  const isHandled = props.handled.includes(props.queryName);
  const hasRelevantData =
    props.data &&
    R.any((propName: string) => props.data[propName])(props.propNames);

  const propNames = () => {
    let result = '';
    for (let i = 0; i < props.propNames.length; ++i) {
      const sep = i === props.propNames.length - 1 ? ' or ' : ', ';
      result += `${i > 0 ? sep : ''}${props.propNames[i]}`;
    }
    return result;
  };

  if (isIgnored && isHandled) {
    console.warn(
      `The query ${props.queryName} is both handled and ignored ` +
        `in ${props.storeName}`
    );
  }

  if (props.data && !hasRelevantData && (isHandled || isIgnored)) {
    console.warn(
      `The query ${props.queryName} was ${isIgnored ? 'ignored' : 'handled'} ` +
        `in ${props.storeName} but does not return any ${propNames()}.`
    );
  }

  if (hasRelevantData && !isHandled && !isIgnored) {
    console.warn(
      `The query ${props.queryName} returned ${propNames()} but was not ` +
        `handled or ignored in ${props.storeName}.`
    );
  }

  return isHandled;
};
