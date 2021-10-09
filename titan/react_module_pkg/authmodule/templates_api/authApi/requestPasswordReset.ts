import { apiBase } from 'src/api/ApiBase';
import { States } from 'src/api/authApi/states';
import { isError } from 'src/api/authApi/utils';
import { ObjT } from 'src/utils/types';

export async function requestPasswordReset(email: string) {
  const query = `mutation ($email: String!) {
      requestPasswordReset(
        email: $email,
      ) {
        success,
        errors,
        passwordResetToken
      }
    }`;

  await apiBase.doQuery(
    'requestPasswordReset',
    query,
    {
      email,
    },
    (response: ObjT) => {
      if (isError(['requestPasswordReset', 'errors'])(response))
        return {
          success: false,
          errors: [States.REQUEST_PASSWORD_RESET_FAILED],
        };

      return {
        success: true,
        passwordResetToken: response.requestPasswordReset.passwordResetToken,
      };
    },
    (error: ObjT) => {
      return error.response.errors[0].message;
    }
  );
}
