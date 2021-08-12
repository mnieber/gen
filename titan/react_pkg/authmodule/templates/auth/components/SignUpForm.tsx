import { FormState, FormStateProvider } from 'react-form-state-context';
import { States } from 'src/api/authApi/states';
import { ControlledCheckbox } from 'src/auth/components/formFields';
import { EmailField } from 'src/auth/components/formFields/EmailField';
import { GlobalError } from 'src/auth/components/formFields/GlobalError';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field } from 'src/forms/components/Field';

const getExternalErrors = (errors: Array<string>) => {
  const fieldErrors: { [name: string]: string } = {};
  if (errors?.includes(States.SIGN_UP_FAILED)) {
    fieldErrors['global'] =
      'Sorry, there seems to be a technical problem. ' +
      'Check your internet connection, or try again later.';
  }
  return fieldErrors;
};

type PropsT = {
  signUp: (email: string, acceptsTerms: boolean) => any;
  errors: Array<string>;
};

export function SignUpForm(props: PropsT) {
  const handleValidate = ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values.acceptsTerms) {
      setError('acceptsTerms', 'You need to accept the terms and conditions');
    }
  };

  const handleSubmit = ({ values }: { values: FormState['values'] }) => {
    props.signUp(values.email, values.acceptsTerms);
  };

  return (
    <FormStateProvider
      initialValues={{
        acceptsTerms: false,
        email: null,
      }}
      initialErrors={getExternalErrors(props.errors)}
      handleValidate={handleValidate}
      handleSubmit={handleSubmit}
    >
      <GlobalError />
      <Field fieldName="email" label="Email">
        <EmailField />
      </Field>
      <Field fieldName="acceptsTerms" label="">
        <ControlledCheckbox />
        <p>I agree to the terms and conditions</p>
      </Field>
      <SubmitButton dataCy="signUpBtn" label="Sign Up" />
    </FormStateProvider>
  );
}
