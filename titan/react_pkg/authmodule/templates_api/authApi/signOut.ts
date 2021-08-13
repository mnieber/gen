import { setToken } from 'src/utils/graphqlClient';

export async function signOut() {
  try {
    setToken('');
    return '';
  } catch (e) {
    throw Error('Could not sign out');
  }
}
