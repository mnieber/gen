import React from 'react';
import { FormStateProvider } from 'react-form-state-context';
import { form } from './form';
import { useMessages } from './useMessages';
import { EmailField } from '/src/auth/components/formFields/EmailField';
import { PasswordField } from '/src/auth/components/formFields/PasswordField';
import { SubmitButton } from '/src/auth/components/formFields/SubmitButton';
import { Field, GlobalError } from '/src/forms/components';
import { colSkewer } from '/src/frames/components';
import { cn } from '/src/utils/classnames';

export const formFields = {
  email: 'email',
  password: 'password',
};

export type PropsT = {
  signIn: (email: string, password: string) => any;
  requestMagicLink: (email: string) => any;
  errors: Array<string>;
  className?: any;
};

export function SignInForm(props: PropsT) {
  const { messages } = useMessages();
  const [useMagicLink, setUseMagicLink] = React.useState(false);

  return (
    <FormStateProvider
      initialValues={form.getInitialValues()}
      initialErrors={form.getExternalErrors(messages, props.errors)}
      handleValidate={form.getHandleValidate(useMagicLink, messages)}
      handleSubmit={form.getHandleSubmit(useMagicLink, props)}
    >
      <div
        className={cn(
          'SignInForm',
          colSkewer,
          'items-stretch',
          props.className
        )}
      >
        <GlobalError className="mb-2" />

        <div className={cn('grid grid-cols-[1fr,1fr] gap-x-2')}>
          <label>
            <input
              className={cn('uk-radio', 'mr-2')}
              type="radio"
              value={'password'}
              checked={!useMagicLink}
              onChange={() => setUseMagicLink(false)}
            />
            <span className="ml-2">{messages.divImUsingMyPassword}</span>
          </label>
          <label>
            <input
              className={cn('uk-radio', 'mr-2')}
              data-cy="signInByMagicLinkBtn"
              type="radio"
              value={'magicLink'}
              checked={useMagicLink}
              onChange={() => setUseMagicLink(true)}
            />
            <span className="ml-2">{messages.divImUsingAMagicLink}</span>
          </label>
        </div>

        <Field
          fieldName={formFields.email}
          label="Email"
          useSmartLabel={true}
          tabOnEnter={!useMagicLink}
          submitOnEnter={useMagicLink}
          autoFocus={true}
          className="my-4"
        >
          <EmailField />
        </Field>

        {!useMagicLink && (
          <Field
            fieldName="password"
            label="Password"
            useSmartLabel={true}
            submitOnEnter={true}
            className="my-4"
          >
            <PasswordField placeholder={messages.divEnterYourPassword} />
          </Field>
        )}

        <SubmitButton
          dataCy={useMagicLink ? 'sendMagicLinkBtn' : 'signInBtn'}
          label={
            useMagicLink
              ? messages.labelSendMeTheMagicLink
              : messages.labelSignIn
          }
          className={cn('place-self-center', 'my-4')}
        />
      </div>
    </FormStateProvider>
  );
}
