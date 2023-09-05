import React from 'react';
import { cn } from '/src/utils/classnames';

// Import styles
import './AuthPage.scss';

type PropsT = React.PropsWithChildren<{}>;

export const AuthPage = (props: PropsT) => {
  return <div className={cn('AuthPage')}>{props.children}</div>;
};

// An AuthPage has:
// - a LogoCard that appears on the left, e.g. 'Welcome to vidlito'.
// - a Gap that separates the LogoCard from the AuthCard.
// - an AuthCard on the right, e.g. a card for signing in.
export const AuthPageS = {
  Gap: () => 'AuthPage__Gap',
};
