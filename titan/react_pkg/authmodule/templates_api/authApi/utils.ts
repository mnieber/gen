import * as R from 'ramda';
import { ObjT } from 'src/utils/types';

export const hasErrorCode = (
  path: string[],
  code: string
): ((response: ObjT) => boolean) =>
  R.pipe(R.pathOr([], path), R.includes(code));

export const isError = (path: string[]): ((response: ObjT) => boolean) =>
  R.pipe(R.pathOr([], path), R.complement(R.isEmpty));
