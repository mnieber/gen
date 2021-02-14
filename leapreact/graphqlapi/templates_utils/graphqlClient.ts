import { GraphQLClient } from 'graphql-request';

function _createClient() {
  const authToken = localStorage.getItem('authToken');

  return new GraphQLClient(`http://${window.location.hostname}:8000/graphql/`, {
    headers: authToken
      ? {
          Authorization: 'JWT ' + authToken,
        }
      : {},
  });
}

let _graphqlClient = _createClient();

export const graphqlClient = () => _graphqlClient;
export const setToken = (authToken: string) => {
  localStorage.setItem('authToken', authToken);
  _graphqlClient = _createClient();
};

export function doQuery(query: string, variables: any) {
  return graphqlClient().request(query, variables);
}
