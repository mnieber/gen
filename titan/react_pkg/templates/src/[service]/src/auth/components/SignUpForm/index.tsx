import { FormStateProvider } from 'react-form-state-context';
import { form } from './form';
import { useMessages } from './useMessages';
import { AuthFormS } from '/src/auth/components/AuthForm';
import {
  ControlledCheckbox,
  EmailField,
  Field,
  FormSaveButton,
  GlobalError,
} from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

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
      {
        // 🔳 SignUpForm 🔳
      }
      <div className={cn('SignInForm', [L.col.banner(), props.className])}>
        {
          // 🔳 Global error 🔳
        }
        <GlobalError className={AuthFormS.GlobalError()} />

        {
          // 🔳 EmailField 🔳
        }
        <Field fieldName={formFields.email} className={AuthFormS.Field()}>
          <EmailField autoFocus={true} placeholder="Email" />
        </Field>

        {
          // 🔳 TermsField 🔳
        }
        <Field
          fieldName={formFields.acceptsTerms}
          className={AuthFormS.Field()}
        >
          <div className={cn('SignUpForm__Terms', [L.row.skewer()])}>
            <ControlledCheckbox />
            <div className={cn('ml-2')}>{messages.divIAgreeToTheTerms}</div>
          </div>
        </Field>

        {
          // 🔳 FormSaveButton 🔳
        }
        <FormSaveButton
          dataCy="signUpBtn"
          label="Sign Up"
          className={cn(AuthFormS.Button())}
        />
      </div>
    </FormStateProvider>
  );
}
