import React from 'react';
import { States } from 'src/auth/api/states';
import { AuthState } from 'src/auth/AuthState';

export const AuthStateContext = React.createContext<AuthState | undefined>(
  undefined
);

type PropsT = React.PropsWithChildren<{}>;

export const AuthStateProvider = (props: PropsT) => {
  const [authState] = React.useState(() => new AuthState(States.INITIAL));

  return (
    <AuthStateContext.Provider value={authState}>
      {props.children}
    </AuthStateContext.Provider>
  );
};
