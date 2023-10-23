import React from 'react';
import { AuthState } from '/src/auth/AuthState';
import { States } from '/src/auth/endpoints/states';
import { useBuilder } from '/src/utils/hooks/useBuilder';

export const AuthStateContext = React.createContext<AuthState | undefined>(
  undefined
);

type PropsT = React.PropsWithChildren<{}>;

export const AuthStateProvider = (props: PropsT) => {
  const authState = useBuilder(() => new AuthState(States.INITIAL));

  return (
    <AuthStateContext.Provider value={authState}>
      {props.children}
    </AuthStateContext.Provider>
  );
};
