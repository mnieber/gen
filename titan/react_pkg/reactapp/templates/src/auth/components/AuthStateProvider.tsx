import React from 'react';
import { States } from 'src/api/authApi/states';
import { AuthState } from 'src/auth/AuthState';

export const AuthStateContext = React.createContext<AuthState | undefined>(
  undefined
);

type PropsT = React.PropsWithChildren<{}>;

export const AuthStateProvider: React.FC<PropsT> = (props: PropsT) => {
  const [authState] = React.useState(() => new AuthState(States.INITIAL));

  return (
    <AuthStateContext.Provider value={authState}>
      {props.children}
    </AuthStateContext.Provider>
  );
};
