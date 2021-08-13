import { Signal } from 'micro-signals';
import { action, makeObservable, observable } from 'mobx';
import * as authApi from 'src/api/authApi';
import { States } from 'src/api/authApi/states';
import * as events from 'src/auth/AuthStore/events';
import { AuthStoreEventT } from 'src/auth/AuthStore/events';
import { maybeSetCypressCookie } from 'src/utils/cookies';
import { ObjT } from 'src/utils/types';

const termsVersion: string = process.env.REACT_APP_TERMS_VERSION ?? '1.0.0';

export class Anonymous {}
export const anonymous = new Anonymous();

export class AuthStore {
  @observable signedInUserId: string | Anonymous = anonymous;
  signal: Signal<any> = new Signal();

  constructor() {
    makeObservable(this);
  }

  loadUserId = () => {
    this.signal.dispatch({
      topic: events.LoadUserId,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .loadUserId() //
      .then(
        action((response: ObjT) => {
          if (response.errors) {
            this.signal.dispatch({
              topic: events.LoadUserId,
              payload: {
                state: States.LOAD_USER_ID_FAILED,
                errors: response.errors,
              },
            } as AuthStoreEventT);
          } else {
            this.signedInUserId = response.userId ?? anonymous;
            this.signal.dispatch({
              topic: events.LoadUserId,
              payload: {
                state: States.LOAD_USER_ID_SUCCEEDED,
              },
            } as AuthStoreEventT);
          }
        })
      );
  };

  signIn = (userId: string, password: string) => {
    this.signal.dispatch({
      topic: events.SignIn,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .signIn(userId, password) //
      .then(
        action((response: ObjT) => {
          if (response.errors) {
            this.signal.dispatch({
              topic: events.SignIn,
              payload: {
                errors: response.errors,
                state: States.SIGN_IN_FAILED,
              },
            } as AuthStoreEventT);
          } else {
            this.signedInUserId = response.userId;
            this.signal.dispatch({
              topic: events.SignIn,
              payload: {
                state: States.SIGN_IN_SUCCEEDED,
              },
            } as AuthStoreEventT);
          }
        })
      );
  };

  signUp = (email: string, acceptsTerms: boolean) => {
    this.signal.dispatch({
      topic: events.SignUp,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .signUp(email, acceptsTerms, termsVersion) //
      .then((response: ObjT) => {
        if (response.errors) {
          maybeSetCypressCookie('cypressAccountActivationToken', '');
          this.signal.dispatch({
            topic: events.SignUp,
            payload: { errors: response.errors, state: States.SIGN_UP_FAILED },
          } as AuthStoreEventT);
        } else {
          maybeSetCypressCookie(
            'cypressAccountActivationToken',
            response.activationToken
          );
          this.signal.dispatch({
            topic: events.SignUp,
            payload: {
              state: States.SIGN_UP_SUCCEEDED,
            },
          } as AuthStoreEventT);
        }
      });
  };

  requestPasswordReset = (email: string) => {
    this.signal.dispatch({
      topic: events.ResetPassword,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .requestPasswordReset(email) //
      .then((response: ObjT) => {
        if (response.errors) {
          maybeSetCypressCookie('cypressPasswordResetToken', '');
          this.signal.dispatch({
            topic: events.ResetPassword,
            payload: {
              state: States.REQUEST_PASSWORD_RESET_FAILED,
              errors: response.errors,
            },
          } as AuthStoreEventT);
        } else {
          maybeSetCypressCookie(
            'cypressPasswordResetToken',
            response.passwordResetToken
          );
          this.signal.dispatch({
            topic: events.ResetPassword,
            payload: {
              state: States.REQUEST_PASSWORD_RESET_SUCCEEDED,
            },
          } as AuthStoreEventT);
        }
      });
  };

  resetPassword = (password: string, passwordResetToken: string) => {
    this.signal.dispatch({
      topic: events.ChangePassword,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .resetPassword(password, passwordResetToken) //
      .then((response: ObjT) => {
        if (response.errors) {
          this.signal.dispatch({
            topic: events.ResetPassword,
            payload: {
              state: States.RESET_PASSWORD_FAILED,
              errors: response.errors,
            },
          } as AuthStoreEventT);
        } else {
          this.signal.dispatch({
            topic: events.ResetPassword,
            payload: {
              state: States.RESET_PASSWORD_SUCCEEDED,
            },
          } as AuthStoreEventT);
        }
      });
  };

  activateAccount = (activationToken: string, password: string) => {
    this.signal.dispatch({
      topic: events.ActivateAccount,
      payload: { state: States.INITIATING },
    } as AuthStoreEventT);

    authApi
      .activateAccount(activationToken, password) //
      .then((response: ObjT) => {
        if (response.errors) {
          this.signal.dispatch({
            topic: events.ActivateAccount,
            payload: {
              state: States.ACTIVATE_ACCOUNT_FAILED,
              errors: response.errors,
            },
          } as AuthStoreEventT);
        } else {
          this.signal.dispatch({
            topic: events.ActivateAccount,
            payload: {
              state: States.ACTIVATE_ACCOUNT_SUCCEEDED,
            },
          } as AuthStoreEventT);
        }
      });
  };

  signOut = () => {
    authApi
      .signOut() //
      .then(
        action(() => {
          this.signedInUserId = anonymous;
          this.signal.dispatch({
            topic: events.SignOut,
            payload: {
              state: States.SIGN_OUT_SUCCEEDED,
            },
          } as AuthStoreEventT);
        })
      );
  };
}
