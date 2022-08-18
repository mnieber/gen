import jQuery from 'jquery';
import { observer } from 'mobx-react-lite';
import React from 'react';
import { useLoadUserId, useSignOut } from 'src/auth/api';
import { RouterLink } from 'src/routes/components';
import { history } from 'src/routes/components/UrlRouter';
import { useRoutes } from 'src/routes/hooks/useRoutes';
import { cn } from 'src/utils/classnames';
import UIkit from 'uikit';
import './AccountMenu.scss';

type PropsT = React.PropsWithChildren<{}>;

export const AccountMenu: React.FC<PropsT> = observer(() => {
  const routes = useRoutes();
  const signOut = useSignOut().mutateAsync;
  const loadUserId = useLoadUserId();
  const menuRef = React.useRef(null);

  const closeDropDown = () => {
    jQuery(menuRef.current as any).hide();
  };

  const signInDiv = (
    <li className="uk-active">
      <RouterLink to={routes.signIn()} onClick={closeDropDown}>
        Sign in
      </RouterLink>
    </li>
  );

  const signOutDiv = (
    <li className="uk-active">
      <RouterLink
        dataCy="signOutMenuItem"
        to={routes.signIn()}
        onClick={() =>
          signOut({}).then(() => {
            closeDropDown();
            history.push(routes.signIn());
          })
        }
      >
        Sign out
      </RouterLink>
    </li>
  );

  return (
    <div className={cn('AccountMenu', 'uk-inline')}>
      <button
        data-cy="accountMenu"
        className="uk-button uk-button-default"
        type="button"
      >
        Account
      </button>
      <div
        ref={(elm: any) => {
          menuRef.current = elm;
          UIkit.dropdown(elm, {
            animation: 'uk-animation-slide-top-small',
            duration: 100,
            mode: 'click',
            'delay-hide': 100,
          });
        }}
      >
        <ul className="uk-nav uk-dropdown-nav">
          {!loadUserId.data?.isAuthenticated && signInDiv}
          {loadUserId.data?.isAuthenticated && signOutDiv}
        </ul>
      </div>
    </div>
  );
});
