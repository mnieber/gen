import { FormStateProvider } from 'react-form-state-context';
import { form } from './form';
import { useMessages } from './useMessages';
import { AuthFormS } from '/src/auth/components/AuthForm';
import {
  EmailField,
  Field,
  FormSaveButton,
  GlobalError,
  PasswordField,
} from '/src/forms/components';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';

export const formFields = {
  email: 'email',
  password: 'password',
};

export type PropsT = {
  signIn: (email: string, password: string) => any;
  errors: Array<string>;
  className?: any;
};

export function SignInForm(props: PropsT) {
  const { messages } = useMessages();

  return (
    //
    // 🔳 FormStateProvider 🔳
    //
    <FormStateProvider
      initialValues={form.getInitialValues()}
      initialErrors={form.getExternalErrors(messages, props.errors)}
      handleValidate={form.getHandleValidate(messages)}
      handleSubmit={form.getHandleSubmit(props)}
    >
      {
        // 🔳 SignInForm 🔳
      }
      <div className={cn('SignInForm', [L.col.banner(), props.className])}>
        <GlobalError className={AuthFormS.GlobalError()} />

        {
          // 🔳 EmailField 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName={formFields.email}
          tabOnEnter={true}
        >
          <EmailField autoFocus={true} placeholder="Email" />
        </Field>

        {
          // 🔳 PasswordField 🔳
        }
        <Field
          className={AuthFormS.Field()}
          fieldName="password"
          submitOnEnter={true}
        >
          <PasswordField placeholder="Password" />
        </Field>

        {
          // 🔳 FormSaveButton 🔳
        }
        <FormSaveButton
          dataCy={'signInBtn'}
          label={messages.labelSignIn}
          className={cn(AuthFormS.Button())}
        />
      </div>
    </FormStateProvider>
  );
}
