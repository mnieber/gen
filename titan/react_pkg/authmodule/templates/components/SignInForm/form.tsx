import { FormState } from 'react-form-state-context';
import { States } from 'src/auth/api/states';
import { createFormErrorsObject } from 'src/forms/utils/createFormErrorsObject';
import { ObjT } from 'src/utils/types';
import { formFields as ff, PropsT } from './index';

export const getExternalErrors = (messages: ObjT, errors: Array<string>) => {
  const fieldErrors = createFormErrorsObject();

  if (errors?.includes(States.INVALID_CREDENTIALS)) {
    fieldErrors['global'] = messages.divSignInFailedPleaseCheckEmailAndPassword;
  }
  if (errors?.includes(States.SIGN_IN_FAILED)) {
    fieldErrors['global'] = messages.divSorryThereSeemsToBeATechnicalProblem;
  }
  return fieldErrors;
};

const getInitialValues = () => {
  return {
    [ff.email]: null,
    [ff.password]: null,
  };
};

const getHandleValidate =
  (useMagicLink: boolean, messages: ObjT) =>
  ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values[ff.email]) {
      setError(ff.email, messages.divPleaseEnterYourEmailAddress);
    }
    if (!useMagicLink && !values[ff.password]) {
      setError(ff.password, messages.divPleaseEnterYourPassword);
    }
  };

const getHandleSubmit =
  (useMagicLink: boolean, props: PropsT) =>
  ({ values }: { values: FormState['values'] }) => {
    if (useMagicLink) {
      return props.requestMagicLink(values[ff.email]);
    } else {
      return props.signIn(values[ff.email], values[ff.password]);
    }
  };

export const form = {
  getExternalErrors,
  getInitialValues,
  getHandleValidate,
  getHandleSubmit,
};
