import { EventT } from 'src/utils/events';
import { ObjT } from 'src/utils/types';

export type AuthStoreEventT = EventT & {
  payload: ObjT & {
    state: string;
    errors?: string[];
  };
};

export const ActivateAccount = 'ActivateAccount';
export const ChangePassword = 'ChangePassword';
export const LoadUserId = 'LoadUserId';
export const ResetPassword = 'ResetPassword';
export const SignIn = 'SignIn';
export const SignOut = 'SignOut';
export const SignUp = 'SignUp';
