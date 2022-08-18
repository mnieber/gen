import { toJS } from 'mobx';
import { map } from 'ramda';

const isLogging = process.env.NODE_ENV === 'development';

export function log(msg: string, ...args: any[]) {
  if (isLogging) {
    console.log(`%c ${msg}`, 'color: gray', args);
  }
}

export function logJS(...args: any[]) {
  if (isLogging) {
    console.log(...map(toJS, args));
  }
}
