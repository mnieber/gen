import { toJS } from 'mobx';
import { map } from 'ramda';

const is_logging = process.env.NODE_ENV === 'development';

export function log(msg: string, ...args: any[]) {
  if (is_logging) {
    console.log(`%c ${msg}`, 'color: gray', args);
  }
}

export function logJS(...args: any[]) {
  if (is_logging) {
    console.log(...map(toJS, args));
  }
}
