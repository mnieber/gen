import { apiBase } from 'src/api/ApiBase';
import { setToken } from 'src/utils/graphqlClient';

export async function signOut() {
  await apiBase.doQuery(
    'signOut',
    () => {
      setToken('');
    },
    {}
  );
}
