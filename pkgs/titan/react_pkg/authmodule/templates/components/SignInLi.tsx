import React from 'react';
import { RouterLink } from 'src/routes/components';
import { useRoutes } from 'src/routes/hooks/useRoutes';

type PropsT = {
  menuRef: any;
};

export const SignInLi = (props: PropsT) => {
  const routes = useRoutes();

  return (
    <li className="uk-active">
      <RouterLink to={routes.signIn()} onClick={props.menuRef.closeDropDown}>
        Sign in
      </RouterLink>
    </li>
  );
};
