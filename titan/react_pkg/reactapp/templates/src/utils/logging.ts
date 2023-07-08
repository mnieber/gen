import { toJS } from 'mobx';
import { map } from 'ramda';

const isLogging = import.meta.env.DEV;

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
