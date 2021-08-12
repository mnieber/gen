import { FormState, FormStateProvider } from 'react-form-state-context';
import { States } from 'src/api/authApi/states';
import { EmailField } from 'src/auth/components/formFields/EmailField';
import { GlobalError } from 'src/auth/components/formFields/GlobalError';
import { PasswordField } from 'src/auth/components/formFields/PasswordField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field } from 'src/forms/components/Field';

const getExternalErrors = (errors: Array<string>) => {
  const fieldErrors: { [name: string]: string } = {};
  if (errors?.includes(States.INVALID_CREDENTIALS)) {
    fieldErrors['global'] =
      'SignIn failed, please check your email and password';
  }
  if (errors?.includes(States.SIGN_IN_FAILED)) {
    fieldErrors['global'] =
      'Sorry, there seems to be a technical problem. ' +
      'Check your internet connection, or try again later.';
  }
  return fieldErrors;
};

type SignInFormPropsT = {
  signIn: (email: string, password: string) => any;
  errors: Array<string>;
};

export function SignInForm(props: SignInFormPropsT) {
  const handleValidate = ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values.password) {
      setError('password', 'Please enter your password');
    }
  };

  const handleSubmit = ({ values }: { values: FormState['values'] }) => {
    props.signIn(values.email, values.password);
  };

  return (
    <FormStateProvider
      initialValues={{
        email: null,
        password: null,
      }}
      initialErrors={getExternalErrors(props.errors)}
      handleValidate={handleValidate}
      handleSubmit={handleSubmit}
    >
      <GlobalError />
      <Field fieldName="email" label="Email">
        <EmailField />
      </Field>
      <Field fieldName="password" label="Password">
        <PasswordField placeholder="Enter your password" />
      </Field>
      <SubmitButton dataCy="signInBtn" label="Sign in" />
    </FormStateProvider>
  );
}
