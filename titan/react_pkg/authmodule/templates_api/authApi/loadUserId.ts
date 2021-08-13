import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export async function loadUserId() {
  const query = `query {
        username
      }`;
  const response: ObjT = await doQuery(query, {});
  return {
    userId: response.username,
  };
}
