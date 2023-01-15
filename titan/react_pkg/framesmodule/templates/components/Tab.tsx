/* eslint-disable */

import React from 'react';
import { cn } from 'src/utils/classnames';

export type PropsT = React.PropsWithChildren<{
  active?: boolean;
  disabled?: boolean;
  [k: string]: any;
}>;

export const Tab = (props: PropsT) => {
  const { children, active, disabled, ...others } = props;
  return (
    <li
      className={cn(active ? 'uk-active' : '', disabled ? 'uk-disabled' : '')}
      {...others}
    >
      <a href="#">{props.children}</a>
    </li>
  );
};

/* eslint-enable */
