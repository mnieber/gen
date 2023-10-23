import { FormState } from 'react-form-state-context';
import { formFields as ff, PropsT } from './index';
import { States } from '/src/auth/endpoints/states';
import { createFormErrorsObject } from '/src/forms/utils/createFormErrorsObject';
import { ObjT } from '/src/utils/types';

const getInitialValues = () => {
  return {
    [ff.acceptsTerms]: false,
    [ff.email]: null,
  };
};

const getExternalErrors = (messages: ObjT, errors: Array<string>) => {
  const fieldErrors = createFormErrorsObject();

  if (errors?.includes(States.SIGN_UP_FAILED)) {
    fieldErrors['global'] = messages.divSorryThereSeemsToBeATechnicalProblem;
  }
  return fieldErrors;
};

const getHandleValidate =
  (messages: ObjT) =>
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
    if (!values[ff.acceptsTerms]) {
      setError(
        ff.acceptsTerms,
        messages.divYouNeedToAcceptTheTermsAndConditions
      );
    }
  };

const getHandleSubmit =
  (props: PropsT) =>
  ({ values }: { values: FormState['values'] }) => {
    return props.signUp(values[ff.email], values[ff.acceptsTerms]);
  };

export const form = {
  getExternalErrors,
  getInitialValues,
  getHandleValidate,
  getHandleSubmit,
};
