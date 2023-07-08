import { action, computed, makeObservable, observable } from 'mobx';
import * as R from 'ramda';
import { States } from '/src/auth/endpoints/states';
import { ObjT } from '/src/utils/types';

const lutSuccess: ObjT = {
  signIn: States.SIGN_IN_SUCCEEDED,
  loadUserId: States.LOAD_USER_ID_SUCCEEDED,
  signUp: States.SIGN_UP_SUCCEEDED,
  requestPasswordReset: States.REQUEST_PASSWORD_RESET_SUCCEEDED,
  resetPassword: States.RESET_PASSWORD_SUCCEEDED,
  activateAccount: States.ACTIVATE_ACCOUNT_SUCCEEDED,
  signOut: States.SIGN_OUT_SUCCEEDED,
  requestMagicLink: States.REQUEST_MAGIC_LINK_SUCCEEDED,
  signInByMagicLink: States.SIGN_IN_BY_MAGIC_LINK_SUCCEEDED,
};

const lutFailure: ObjT = {
  signIn: States.SIGN_IN_FAILED,
  loadUserId: States.LOAD_USER_ID_FAILED,
  signUp: States.SIGN_UP_FAILED,
  requestPasswordReset: States.REQUEST_PASSWORD_RESET_FAILED,
  resetPassword: States.RESET_PASSWORD_FAILED,
  activateAccount: States.ACTIVATE_ACCOUNT_FAILED,
  signOut: States.SIGN_OUT_FAILED,
  requestMagicLink: States.REQUEST_MAGIC_LINK_FAILED,
  signInByMagicLink: States.SIGN_IN_BY_MAGIC_LINK_FAILED,
};

export class AuthState {
  @observable errors: string[] = [];
  @observable initialState: string;
  @observable state: string;
  @observable details: ObjT = {};

  constructor(initialState: string) {
    makeObservable(this);
    this.state = this.initialState = initialState;
  }

  @computed get hasErrors() {
    return !R.isEmpty(this.errors);
  }

  @action reset = () => {
    this.errors = [];
    this.state = this.initialState;
    this.details = {};
  };

  isTrackedQuery = (queryName: string) => {
    return [
      'signIn',
      'signUp',
      'requestPasswordReset',
      'resetPassword',
      'activateAccount',
      'signOut',
      'requestMagicLink',
      'signInByMagicLink',
    ].includes(queryName);
  };

  @action onUpdated(queryName: string, data: ObjT) {
    if (this.isTrackedQuery(queryName)) {
      this.errors = data.errors ?? [];
      this.state = data.errors
        ? (lutFailure[queryName] as string)
        : (lutSuccess[queryName] as string);
    }
  }

  @action onUpdating(queryName: string) {
    if (this.isTrackedQuery(queryName)) {
      this.reset();
    }
  }

  @action onErrored(queryName: string, message: string) {
    if (this.isTrackedQuery(queryName)) {
      this.details = { message: message };
      this.errors = [lutFailure[queryName]];
      this.state = lutFailure[queryName];
    }
  }
}
