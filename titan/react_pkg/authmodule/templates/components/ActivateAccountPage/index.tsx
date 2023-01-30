import { observer } from 'mobx-react-lite';
import React from 'react';
import { useParams } from 'react-router-dom';
import { useActivateAccount } from 'src/auth/api';
import { States } from 'src/auth/api/states';
import { ActivateAccountForm } from 'src/auth/components/ActivateAccountForm';
import { AuthFrame } from 'src/auth/components/AuthFrame';
import { useAuthStateContext } from 'src/auth/hooks';
import { ObjT } from 'src/utils/types';
import { useMessages } from './useMessages';

export const ActivateAccountPage = observer(() => {
  const { messages } = useMessages();
  const params = useParams() as ObjT;
  const authState = useAuthStateContext(true);
  const activateAccount = useActivateAccount(authState).mutateAsync;

  const activateAccountForm = (
    <ActivateAccountForm
      activateAccount={(password: string) =>
        activateAccount({ password, activationToken: params.activationToken })
      }
      errors={authState.errors}
    />
  );

  // Note that if we show the activateAccountForm and the user submits the form,
  // then the authState will be updated which causes this component to also re-render.

  return (
    <AuthFrame header="Activate your account" id="ActivateAccountPage">
      <div id="ActivateAccountPage" className="">
        {authState.state === States.ACTIVATE_ACCOUNT_SUCCEEDED && (
          <div>{messages.yourAccountWasActivated}</div>
        )}
        {authState.state !== States.ACTIVATE_ACCOUNT_SUCCEEDED &&
          activateAccountForm}
      </div>
    </AuthFrame>
  );
});
