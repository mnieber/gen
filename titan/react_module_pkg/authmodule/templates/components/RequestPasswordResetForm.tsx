import {
  FormStateProvider,
  HandleSubmitArgsT,
  HandleValidateArgsT,
} from 'react-form-state-context';
import { States } from 'src/api/authApi/states';
import { EmailField } from 'src/auth/components/formFields/EmailField';
import { GlobalError } from 'src/auth/components/formFields/GlobalError';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field } from 'src/forms/components/Field';

const getExternalErrors = (errors: Array<string>) => {
  const fieldErrors: { [name: string]: string } = {};
  if (errors?.includes(States.REQUEST_PASSWORD_RESET_FAILED)) {
    fieldErrors['global'] =
      'Sorry, there seems to be a technical problem. ' +
      'Check your internet connection, or try again later.';
  }
  return fieldErrors;
};

type PasswordResetFormPropsT = {
  requestPasswordReset: (email: string) => any;
  errors: Array<string>;
};

export function RequestPasswordResetForm(props: PasswordResetFormPropsT) {
  const handleValidate = ({ values, setError }: HandleValidateArgsT) => {
    if (!values.email) {
      setError('email', 'Please enter your email address');
    }
  };

  const handleSubmit = ({ values }: HandleSubmitArgsT) => {
    props.requestPasswordReset(values.email);
  };

  return (
    <FormStateProvider
      initialValues={{ email: null }}
      initialErrors={getExternalErrors(props.errors)}
      handleValidate={handleValidate}
      handleSubmit={handleSubmit}
    >
      <GlobalError />
      <div>
        <Field fieldName="email" label="Email">
          <EmailField />
        </Field>
        Enter your email to reset your password.
      </div>
      <SubmitButton dataCy="passwordResetBtn" label="Request password reset" />
    </FormStateProvider>
  );
}
