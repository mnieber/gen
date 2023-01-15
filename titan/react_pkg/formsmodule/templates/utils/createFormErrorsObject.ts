import * as R from 'ramda';
import { ObjT } from 'src/utils/types';

export const createFormErrorsObject = (): ObjT => {
  const formErrors: ObjT = {};
  formErrors.toJSON = () => JSON.stringify(R.keys(formErrors));
  return formErrors;
};
