import { action, computed, makeObservable, observable } from 'mobx';
import * as R from 'ramda';
import { States } from 'src/api/authApi/states';
import { storeConnectsToApi } from 'src/app/AppStore/policies';
import { isErroredRS, isUpdatedRS, isUpdatingRS, RST } from 'src/utils/RST';
import { ObjT } from 'src/utils/types';

const lutSuccess: ObjT = {
  signIn: States.SIGN_IN_SUCCEEDED,
  loadUserId: States.LOAD_USER_ID_SUCCEEDED,
  signUp: States.SIGN_UP_SUCCEEDED,
  requestPasswordReset: States.REQUEST_PASSWORD_RESET_SUCCEEDED,
  resetPassword: States.RESET_PASSWORD_SUCCEEDED,
  activateAccount: States.ACTIVATE_ACCOUNT_SUCCEEDED,
  signOut: States.SIGN_OUT_SUCCEEDED,
};

const lutFailure: ObjT = {
  signIn: States.SIGN_IN_FAILED,
  loadUserId: States.LOAD_USER_ID_FAILED,
  signUp: States.SIGN_UP_FAILED,
  requestPasswordReset: States.REQUEST_PASSWORD_RESET_FAILED,
  resetPassword: States.RESET_PASSWORD_FAILED,
  activateAccount: States.ACTIVATE_ACCOUNT_FAILED,
  signOut: States.SIGN_OUT_FAILED,
};

export class AuthState {
  @observable errors: string[] = [];
  @observable initialState: string;
  @observable state: string;
  @observable details: ObjT = {};

  constructor(initialState: string) {
    makeObservable(this);
    this.state = this.initialState = initialState;
    storeConnectsToApi(this);
  }

  @computed get hasErrors() {
    return !R.isEmpty(this.errors);
  }

  @action reset = () => {
    this.errors = [];
    this.state = this.initialState;
    this.details = {};
  };

  @action onLoadData(rs: RST, queryName: string, vars: ObjT, data: ObjT) {
    if (
      [
        'signIn',
        'signUp',
        'requestPasswordReset',
        'resetPassword',
        'activateAccount',
        'signOut',
      ].includes(queryName)
    ) {
      if (isUpdatingRS(rs)) {
        this.reset();
      }
      if (isUpdatedRS(rs)) {
        this.errors = data.errors ?? [];
        this.state = data.errors
          ? (lutFailure[queryName] as string)
          : (lutSuccess[queryName] as string);
      }
      if (isErroredRS(rs)) {
        this.details = { message: rs.message };
        this.errors = [lutFailure[queryName]];
        this.state = lutFailure[queryName];
      }
    }
  }
}
