import React from 'react';
import { States } from 'src/api/authApi/states';
import { useStore } from 'src/app/components';
import { AuthState } from 'src/auth/AuthState';

export const AuthStateContext = React.createContext<AuthState | undefined>(
  undefined
);

type PropsT = React.PropsWithChildren<{}>;

export const AuthStateProvider: React.FC<PropsT> = (props: PropsT) => {
  const { authStore } = useStore();
  const [authState] = React.useState(
    () => new AuthState(authStore, States.INITIAL)
  );

  return (
    <AuthStateContext.Provider value={authState}>
      {props.children}
    </AuthStateContext.Provider>
  );
};
