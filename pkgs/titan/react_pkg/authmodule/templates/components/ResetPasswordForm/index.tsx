import { FormStateProvider } from 'react-form-state-context';
import { PasswordField } from 'src/auth/components/formFields/PasswordField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field, GlobalError } from 'src/forms/components';

import { form } from './form';
import { useMessages } from './useMessages';

export const formFields = {
  password: 'password',
};

export type PropsT = {
  resetPassword: (password: string) => any;
  errors: Array<string>;
};

export function ResetPasswordForm(props: PropsT) {
  const { messages } = useMessages();

  return (
    <FormStateProvider
      initialValues={form.getInitialValues()}
      initialErrors={form.getExternalErrors(messages, props.errors)}
      handleValidate={form.getHandleValidate(messages)}
      handleSubmit={form.getHandleSubmit(props)}
    >
      <div className="ResetPasswordForm">
        <GlobalError className="mb-4" />
        <Field
          fieldName={formFields.password}
          label="Password"
          useSmartLabel={true}
          submitOnEnter={true}
        >
          <PasswordField placeholder="Enter your password" />
        </Field>
        <div className="my-4">{}</div>{' '}
        <SubmitButton dataCy="passwordChangeBtn" label="Change password" />
      </div>
    </FormStateProvider>
  );
}
