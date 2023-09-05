import { observer } from 'mobx-react-lite';
import { useParams } from 'react-router-dom';
import { useMessages } from './useMessages';
import { ActivateAccountForm } from '/src/auth/components/ActivateAccountForm';
import { AuthCard, AuthCardS } from '/src/auth/components/AuthCard';
import { useActivateAccount } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { useAuthStateContext } from '/src/auth/hooks';
import { cn } from '/src/utils/classnames';
import { ObjT } from '/src/utils/types';

export const ActivateAccountCard = observer(() => {
  const { messages } = useMessages();
  const params = useParams() as ObjT;
  const authState = useAuthStateContext(true);
  const activateAccount = useActivateAccount(authState).mutateAsync;

  // Note that if we show the activateAccountForm and the user submits the form,
  // then the authState will be updated which causes this component to also re-render.

  return (
    <AuthCard id="ActivateAccountCard">
      {authState.state === States.ACTIVATE_ACCOUNT_SUCCEEDED && (
        <div>{messages.yourAccountWasActivated}</div>
      )}
      {authState.state !== States.ACTIVATE_ACCOUNT_SUCCEEDED && (
        <>
          <ActivateAccountForm
            activateAccount={(username: string, password: string) =>
              activateAccount({
                username,
                password,
                activationToken: params.activationToken,
              })
            }
            errors={authState.errors}
          />
          <div className={cn(AuthCardS.CardFooter())}>
            {messages.ifYouAlreadyHaveAnAccount}
          </div>
        </>
      )}
    </AuthCard>
  );
});
