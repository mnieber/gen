import { apiBase } from 'src/api/ApiBase';
import { setToken } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export async function signOut() {
  const query = '';
  await apiBase.doQuery(
    'signOut',
    query,
    {},
    (response: ObjT) => {
      setToken('');
    },
    (error: ObjT) => {
      return 'Could not sign out';
    }
  );
}
