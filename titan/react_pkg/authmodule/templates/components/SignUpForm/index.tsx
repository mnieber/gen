import { FormStateProvider } from 'react-form-state-context';
import { EmailField } from 'src/auth/components/formFields/EmailField';
import { SubmitButton } from 'src/auth/components/formFields/SubmitButton';
import { ControlledCheckbox, Field, GlobalError } from 'src/forms/components';
import { colSkewer } from 'src/frames/components';
import { cn } from 'src/utils/classnames';
import { form } from './form';
import './SignUpForm.scss';
import { useMessages } from './useMessages';

export const formFields = {
  email: 'email',
  acceptsTerms: 'acceptsTerms',
};

export type PropsT = {
  signUp: (email: string, acceptsTerms: boolean) => any;
  errors: Array<string>;
  className?: any;
};

export function SignUpForm(props: PropsT) {
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
          'SignInForm',
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
          autoFocus={true}
          className="my-4"
        >
          <EmailField />
        </Field>

        <Field
          fieldName={formFields.acceptsTerms}
          label=""
          className={cn('my-4')}
        >
          <div className={cn('flex flex-row items-center')}>
            <ControlledCheckbox />
            <p className={cn('SignUpForm__TermsLabel', 'ml-4')}>
              {messages.divIAgreeToTheTerms}
            </p>
          </div>
        </Field>

        <SubmitButton
          dataCy="signUpBtn"
          label="Sign Up"
          className={cn('place-self-center', 'my-4')}
        />
      </div>
    </FormStateProvider>
  );
}
