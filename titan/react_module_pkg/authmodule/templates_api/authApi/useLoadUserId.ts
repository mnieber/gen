import { useMutation } from 'react-query';
import { doQuery } from 'src/utils/graphqlClient';
import { ObjT } from 'src/utils/types';

export function loadUserId() {
  return doQuery(
    `query {
        username
      }`,
    {}
  )
    .then((response: ObjT) => {
      return {
        userId: response.username,
      };
    })
    .catch((error: ObjT) => {
      return error.response.errors[0].message;
    });
}

export const useLoadUserId = () => {
  return useMutation(['loadUserId'], loadUserId, {
    onSuccess: (data: ObjT) => {},
  });
};
