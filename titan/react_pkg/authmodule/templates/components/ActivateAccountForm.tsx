import { FormState, FormStateProvider } from 'react-form-state-context';
import { useParams } from 'react-router-dom';
import { States } from 'src/api/authApi/states';
import { routes } from 'src/app/routeTable';
import { GlobalError } from 'src/auth/components/formFields/GlobalError';
import { PasswordField } from 'src/auth/components/formFields/PasswordField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field } from 'src/forms/components/Field';
import { ObjT } from 'src/utils/types';
import { RouterLink } from 'src/widgets/components/RouterLink';

const _password_too_short_msg = 'Sorry, that password is too short';

const _tokenNotFoundDiv = (
  <div>
    The activation failed, probably because your account is already active.{' '}
    Please try to <RouterLink to={routes.signIn()}>sign in</RouterLink> or{' '}
    <RouterLink to={routes.requestPasswordReset()}>
      reset your password
    </RouterLink>
    .
  </div>
);

const getExternalErrors = (errors: Array<string>) => {
  const fieldErrors: ObjT = {};
  if (errors?.includes(States.PASSWORD_TOO_SHORT)) {
    fieldErrors['password'] = _password_too_short_msg;
  }
  if (errors?.includes(States.ACTIVATION_TOKEN_NOT_FOUND)) {
    fieldErrors['global'] = _tokenNotFoundDiv;
  }
  if (errors?.includes(States.ACTIVATE_ACCOUNT_FAILED)) {
    fieldErrors['global'] =
      'Sorry, there seems to be a technical problem. ' +
      'Check your internet connection, or try again later.';
  }
  return fieldErrors;
};

type PropsT = {
  activateAccount: (email: string, password: string) => any;
  errors: Array<string>;
};

export function ActivateAccountForm(props: PropsT) {
  const params = useParams();

  const handleValidate = ({
    values,
    setError,
  }: {
    values: FormState['values'];
    setError: FormState['setError'];
  }) => {
    if (!values.password) {
      setError('password', 'Please provide a new password');
    } else if (values.password.length < 8) {
      setError('password', _password_too_short_msg);
    }
  };

  const handleSubmit = ({ values }: { values: FormState['values'] }) => {
    props.activateAccount(values.activationToken, values.password);
  };

  const explanationDiv = (
    <div>
      You are one step away from activating your account. To proceed, please
      choose a new password.
    </div>
  );

  return (
    <FormStateProvider
      initialValues={{
        activationToken: (params as any).activationToken,
        password: null,
      }}
      initialErrors={getExternalErrors(props.errors)}
      handleValidate={handleValidate}
      handleSubmit={handleSubmit}
    >
      <GlobalError />
      {explanationDiv}
      <Field fieldName="password" label="Password">
        <PasswordField placeholder="Choose a password" />
      </Field>
      <SubmitButton dataCy="activateAccountBtn" label="Activate account" />
    </FormStateProvider>
  );
}
