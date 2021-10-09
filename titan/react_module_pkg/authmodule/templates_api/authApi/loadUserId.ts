import { apiBase } from 'src/api/ApiBase';
import { ObjT } from 'src/utils/types';

export async function loadUserId() {
  const query = `query {
        username
      }`;
  await apiBase.doQuery(
    'loadUserId',
    query,
    {},
    (response: ObjT) => {
      return {
        userId: response.username,
      };
    },
    (error: ObjT) => {
      return error.response.errors[0].message;
    }
  );
}
