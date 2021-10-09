import { apiBase } from 'src/api/ApiBase';
import { States } from 'src/api/authApi/states';
import { hasErrorCode, isError } from 'src/api/authApi/utils';
import { ObjT } from 'src/utils/types';

export async function activateAccount(
  activationToken: string,
  password: string
) {
  const query = `mutation (
      $activationToken: String!,
      $password: String!,
    ) {
      activateAccount(
        activationToken: $activationToken,
        password: $password,
      ) {
        success,
        errors,
      }
    }`;

  await apiBase.doQuery(
    'activateAccount',
    query,
    {
      activationToken,
      password,
    },
    (response: ObjT) => {
      if (
        hasErrorCode(
          ['activateAccount', 'errors', 'password'],
          'TOO_SHORT'
        )(response)
      )
        return {
          success: false,
          errors: [States.PASSWORD_TOO_SHORT],
        };

      if (
        hasErrorCode(
          ['activateAccount', 'errors', 'activationToken'],
          'NOT_FOUND'
        )(response)
      )
        return {
          success: false,
          errors: [States.ACTIVATION_TOKEN_NOT_FOUND],
        };

      if (isError(['activateAccount', 'errors'])(response))
        return {
          success: false,
          errors: [States.ACTIVATE_ACCOUNT_FAILED],
        };

      return {
        success: true,
      };
    },
    (error: ObjT) => {
      return error.response.errors[0].message;
    }
  );
}
