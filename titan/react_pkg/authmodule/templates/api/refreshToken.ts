import { doQuery, getRefreshToken, setToken } from 'src/api/graphqlClient';
import { ObjT } from 'src/utils/types';

export function refreshToken() {
  return doQuery(
    `mutation refreshToken($refreshToken: String!) {
      refreshToken(
        refreshToken: $refreshToken
      ) {
        token,
        refreshToken,
      }
    }`,
    {
      refreshToken: getRefreshToken(),
    }
  ).then((response: ObjT) => {
    const token = response.refreshToken.token;
    const refreshToken = response.refreshToken.refreshToken;
    setToken(token, refreshToken);

    return {
      success: true,
    };
  });
}
