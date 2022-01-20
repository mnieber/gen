import React from 'react';
import { AuthStoreContext } from 'src/auth/components/AuthStoreProvider';

export const useAuthStore = () => {
  const authStore = React.useContext(AuthStoreContext);
  if (!authStore) {
    throw new Error('useAuthStore must be used within a AuthStoreProvider.');
  }
  return authStore;
};
