import React from 'react';
import { AuthState } from 'src/auth/AuthState';
import { AuthStateContext } from 'src/auth/components/AuthStateProvider';

export const useAuthStateContext = (reset: boolean = false): AuthState => {
  const authState = React.useContext(AuthStateContext);
  React.useEffect(() => {
    if (authState && reset) {
      authState.reset();
    }
  }, [authState, reset]);

  if (!authState) {
    throw Error('No auth state');
  }
  return authState;
};
