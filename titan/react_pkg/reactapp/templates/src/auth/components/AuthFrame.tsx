import { observer } from 'mobx-react-lite';
import React from 'react';

// RequestPasswordResetPage

type PropsT = React.PropsWithChildren<{
  header: string;
}>;

export const AuthFrame = observer((props: PropsT) => {
  return (
    <div className="">
      <h1 className="text-lg">{props.header}</h1>
      {props.children}
    </div>
  );
});
