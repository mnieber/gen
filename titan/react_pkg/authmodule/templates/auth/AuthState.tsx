import { action, computed, makeObservable, observable } from 'mobx';
import * as R from 'ramda';
import { AuthStore } from 'src/auth/AuthStore';
import * as AuthStoreEvents from 'src/auth/AuthStore/events';
import { AuthStoreEventT } from 'src/auth/AuthStore/events';
import { ObjT } from 'src/utils/types';

export class AuthState {
  @observable errors: string[] = [];
  @observable initialState: string;
  @observable state: string;
  @observable details: ObjT = {};

  constructor(authStore: AuthStore, initialState: string) {
    makeObservable(this);
    this.state = this.initialState = initialState;
    authStore.signal.add((event: AuthStoreEventT) => this.handleEvent(event));
  }

  @computed get hasErrors() {
    return !R.isEmpty(this.errors);
  }

  @action reset = () => {
    this.errors = [];
    this.state = this.initialState;
    this.details = {};
  };

  @action handleEvent = (event: AuthStoreEventT) => {
    if (event.topic !== AuthStoreEvents.LoadUserId) {
      this.errors = event.payload?.errors ?? [];
      this.state = event.payload.state;
      this.details = event.payload ?? {};
    }
  };
}
