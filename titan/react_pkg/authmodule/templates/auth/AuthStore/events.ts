import { EventT, EventTopic } from 'src/utils/events';
import { ObjT } from 'src/utils/types';

export type AuthStoreEventT = EventT & {
  payload: ObjT & {
    state: string;
    errors?: string[];
  };
};

export const ActivateAccount = new EventTopic('ActivateAccount');
export const ChangePassword = new EventTopic('ChangePassword');
export const LoadUserId = new EventTopic('LoadUserId');
export const ResetPassword = new EventTopic('ResetPassword');
export const SignIn = new EventTopic('SignIn');
export const SignOut = new EventTopic('SignOut');
export const SignUp = new EventTopic('SignUp');
