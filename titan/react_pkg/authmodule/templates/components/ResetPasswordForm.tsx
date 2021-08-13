import { FormState, FormStateProvider } from 'react-form-state-context';
import { States } from 'src/api/authApi/states';
import { GlobalError } from 'src/auth/components/formFields/GlobalError';
import { PasswordField } from 'src/auth/components/formFields/PasswordField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field } from 'src/forms/components/Field';

const getExternalErrors = (errors: Array<string>) => {
  const fieldErrors: { [name: string]: string } = {};
  if (errors?.includes(States.PASSWORD_TOO_SHORT)) {
    fieldErrors['password'] = 'Sorry, that password is too short';
  }
  if (errors?.includes(States.PASSWORD_RESET_EMAIL_UNKNOWN)) {
    fieldErrors['global'] =
      "Sorry, we could not find your account. Don't worry, this could be a technical " +
      'failure on our side. Please contact support.';
  }
  if (errors?.includes(States.RESET_PASSWORD_FAILED)) {
    fieldErrors['global'] =
      'Sorry, there seems to be a technical problem. ' +
      'Check your internet connection, or try again later.';
  }
  return fieldErrors;
};

type PasswordResetFormPropsT = {
  resetPassword: (password: string) => any;
  errors: Array<string>;
};

export function ResetPasswordForm(props: PasswordResetFormPropsT) {
  const handleValidate = ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values.password) {
      setError('password', 'Please provide a new password');
    }
  };

  const handleSubmit = ({ values }: { values: FormState['values'] }) => {
    props.resetPassword(values.password);
  };

  return (
    <FormStateProvider
      initialValues={{ password: null }}
      initialErrors={getExternalErrors(props.errors)}
      handleValidate={handleValidate}
      handleSubmit={handleSubmit}
    >
      <GlobalError />
      <Field fieldName="password" label="Password">
        <PasswordField placeholder="Enter your password" />
      </Field>
      <SubmitButton dataCy="passwordChangeBtn" label="Change password" />
    </FormStateProvider>
  );
}
