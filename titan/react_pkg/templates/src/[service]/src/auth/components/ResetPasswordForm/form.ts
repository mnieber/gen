import { FormState } from 'react-form-state-context';
import { formFields as ff, PropsT } from './index';
import { States } from '/src/auth/endpoints/states';
import { createFormErrorsObject } from '/src/forms/utils/createFormErrorsObject';
import { ObjT } from '/src/utils/types';

export const getExternalErrors = (messages: ObjT, errors: Array<string>) => {
  const fieldErrors = createFormErrorsObject();

  if (errors?.includes(States.PASSWORD_TOO_SHORT)) {
    fieldErrors['password'] = messages.sorryThatPasswordIsTooShort;
  }
  if (errors?.includes(States.PASSWORD_RESET_EMAIL_UNKNOWN)) {
    fieldErrors['global'] = messages.sorryWeCouldNotFindYourAccount;
  }
  if (errors?.includes(States.PASSWORD_RESET_TOKEN_NOT_FOUND)) {
    fieldErrors['global'] = messages.divSorryWeCouldNotResetThePassword;
  }
  if (errors?.includes(States.RESET_PASSWORD_FAILED)) {
    fieldErrors['global'] = messages.divSorryThereSeemsToBeATechnicalProblem;
  }
  return fieldErrors;
};

const getInitialValues = () => {
  return { [ff.password]: null };
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
    if (!values.password) {
      setError('password', messages.divPleaseProvideANewPassword);
    }
  };

const getHandleSubmit =
  (props: PropsT) =>
  ({ values }: { values: FormState['values'] }) => {
    return props.resetPassword(values.password);
  };

export const form = {
  getExternalErrors,
  getInitialValues,
  getHandleValidate,
  getHandleSubmit,
};
