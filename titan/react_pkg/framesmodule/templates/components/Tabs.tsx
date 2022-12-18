import React from 'react';
import UIkit from 'uikit';

export type PropsT = React.PropsWithChildren<{
  [k: string]: any;
}>;

export const Tabs = (props: PropsT) => {
  const { children, ...others } = props;

  return (
    <ul
      ref={(elm: any) => {
        UIkit.tab(elm, {});
      }}
      {...others}
    >
      {props.children}
    </ul>
  );
};
