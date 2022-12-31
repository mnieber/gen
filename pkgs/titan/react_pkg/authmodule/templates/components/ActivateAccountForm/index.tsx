import { FormStateProvider } from 'react-form-state-context';
import { PasswordField } from 'src/auth/components/formFields/PasswordField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field, GlobalError } from 'src/forms/components';
import { cn } from 'src/utils/classnames';
import { form } from './form';
import { useMessages } from './useMessages';

export const formFields = {
  password: 'password',
};

export type PropsT = {
  activateAccount: (password: string) => any;
  errors: Array<string>;
  className?: any;
};

export function ActivateAccountForm(props: PropsT) {
  const { messages } = useMessages();

  return (
    <FormStateProvider
      initialValues={form.getInitialValues()}
      initialErrors={form.getExternalErrors(messages, props.errors)}
      handleValidate={form.getHandleValidate(messages)}
      handleSubmit={form.getHandleSubmit(props)}
    >
      <div
        className={cn(
          'ActivateAccountForm',
          'flex flex-col justify-center',
          props.className
        )}
      >
        <GlobalError className="mb-4" />

        <div>
          {messages.divYouAreOneStepAway}
          <br />
          {messages.divToProceedPleaseChooseANewPassword}
        </div>

        <Field
          fieldName={formFields.password}
          label="Password"
          useSmartLabel={true}
          submitOnEnter={true}
          className="my-4"
        >
          <PasswordField placeholder={'Choose a password'} />
        </Field>

        <SubmitButton
          dataCy="activateAccountBtn"
          label="Activate account"
          className={cn('place-self-center', 'my-4')}
        />
      </div>
    </FormStateProvider>
  );
}