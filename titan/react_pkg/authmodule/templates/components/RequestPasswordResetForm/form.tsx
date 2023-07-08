import {
  HandleSubmitArgsT,
  HandleValidateArgsT,
} from 'react-form-state-context';
import { PropsT, formFields as ff } from './index';
import { States } from '/src/auth/endpoints/states';
import { createFormErrorsObject } from '/src/forms/utils/createFormErrorsObject';
import { ObjT } from '/src/utils/types';

const getExternalErrors = (messages: ObjT, errors: Array<string>) => {
  const fieldErrors = createFormErrorsObject();

  if (errors?.includes(States.REQUEST_PASSWORD_RESET_FAILED)) {
    fieldErrors['global'] = messages.divSorryThereSeemsToBeATechnicalProblem;
  }
  return fieldErrors;
};

const getInitialValues = () => {
  return { [ff.email]: null };
};

const getHandleValidate =
  (messages: ObjT) =>
  ({ values, setError }: HandleValidateArgsT) => {
    if (!values[ff.email]) {
      setError(ff.email, messages.divPleaseEnterYourEmailAddress);
    }
  };

const getHandleSubmit =
  (props: PropsT) =>
  ({ values }: HandleSubmitArgsT) => {
    return props.requestPasswordReset(values[ff.email]);
  };

export const form = {
  getExternalErrors,
  getInitialValues,
  getHandleValidate,
  getHandleSubmit,
};
