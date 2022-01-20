import classnames from 'classnames';
import { observer } from 'mobx-react-lite';
import React from 'react';
import { useSignOut } from 'src/api/authApi';
import { anonymous } from 'src/auth/AuthStore';
import { useAuthStore } from 'src/auth/components/useAuthStore';
import { RouterLink } from 'src/routes/components';
import UIkit from 'uikit';
import './AccountMenu.scss';

const closeDropDown = () => {
  UIkit.dropdown('#AccountMenu').hide();
};

type PropsT = React.PropsWithChildren<{}>;

export const AccountMenu: React.FC<PropsT> = observer(() => {
  const authStore = useAuthStore();
  const signOut = useSignOut().mutateAsync;

  const signInDiv = (
    <li className="uk-active">
      <RouterLink to={'/sign-in'} onClick={closeDropDown}>
        Sign in
      </RouterLink>
    </li>
  );

  const signOutDiv = (
    <li className="uk-active">
      <RouterLink
        dataCy="signOutMenuItem"
        to={'/sign-in'}
        onClick={() => signOut({})}
      >
        Sign out
      </RouterLink>
    </li>
  );

  return (
    <div className={classnames('AccountMenu', 'uk-inline')}>
      <button
        data-cy="accountMenu"
        className="uk-button uk-button-default"
        type="button"
      >
        Account
      </button>
      <div
        id="AccountMenu"
        data-uk-dropdown={
          'animation: uk-animation-slide-top-small; duration: 100; mode: click; ' +
          'delay-hide: 100'
        }
      >
        <ul className="uk-nav uk-dropdown-nav">
          {authStore.signedInUserId === anonymous && signInDiv}
          {authStore.signedInUserId !== anonymous && signOutDiv}
        </ul>
      </div>
    </div>
  );
});
