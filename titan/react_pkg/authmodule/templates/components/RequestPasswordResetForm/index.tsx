import { FormStateProvider } from 'react-form-state-context';
import { EmailField } from 'src/auth/components/formFields/EmailField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { Field, GlobalError } from 'src/forms/components';
import { colSkewer } from 'src/frames/components';
import { cn } from 'src/utils/classnames';
import { form } from './form';
import { useMessages } from './useMessages';

export const formFields = {
  email: 'email',
};

export type PropsT = {
  requestPasswordReset: (email: string) => any;
  errors: Array<string>;
  className?: any;
};

export function RequestPasswordResetForm(props: PropsT) {
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
          'RequestPasswordResetForm',
          colSkewer,
          'items-stretch',
          props.className
        )}
      >
        <GlobalError />

        <Field
          fieldName={formFields.email}
          label="Email"
          useSmartLabel={true}
          submitOnEnter={true}
        >
          <EmailField />
        </Field>

        <div className={cn('place-self-center', 'my-4')}>
          {messages.divEnterYourEmailToResetYourPassword}
        </div>

        <SubmitButton
          dataCy="passwordResetBtn"
          label="Request password reset"
          className={cn('place-self-center', 'my-4')}
        />
      </div>
    </FormStateProvider>
  );
}
