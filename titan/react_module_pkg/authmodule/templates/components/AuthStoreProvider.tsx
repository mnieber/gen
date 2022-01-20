import React from 'react';
import { AuthStore } from 'src/auth/AuthStore';

const authStore = new AuthStore();

export const AuthStoreContext = React.createContext<AuthStore>(authStore);

export const AuthStoreProvider: React.FC = ({ children }) => {
  return (
    <AuthStoreContext.Provider value={authStore}>
      {children}
    </AuthStoreContext.Provider>
  );
};
