import { GraphQLClient } from 'graphql-request';

export const graphqlHostUrl = window.location.host.startsWith('localhost')
  ? import.meta.env.VITE_LOCALHOST_API_ENDPOINT
  : import.meta.env.VITE_BACKEND_API_ENDPOINT ?? '';

function _createClient() {
  if (!graphqlHostUrl) throw Error('No graphql endpoint was configured');

  const authToken = getToken();
  return new GraphQLClient(graphqlHostUrl, {
    headers: authToken
      ? {
          Authorization: 'JWT ' + authToken,
        }
      : {},
  });
}

export const setToken = (
  authToken: string | undefined,
  refreshToken?: string
) => {
  if (authToken === undefined) {
    localStorage.removeItem('authToken');
  } else {
    localStorage.setItem('authToken', authToken);
  }
  if (refreshToken === undefined) {
    localStorage.removeItem('refreshToken');
  } else {
    localStorage.setItem('refreshToken', refreshToken);
  }
  _graphqlClient = _createClient();
};

export const getToken = () => {
  return localStorage.getItem('authToken');
};

export const getRefreshToken = () => {
  return localStorage.getItem('refreshToken');
};

export function doQuery(query: string, variables: any) {
  return graphqlClient().request(query, variables);
}

let _graphqlClient = _createClient();

export const graphqlClient = () => _graphqlClient;
