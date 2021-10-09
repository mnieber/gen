import { apiBase } from 'src/api/ApiBase';
import { States } from 'src/api/authApi/states';
import { isError } from 'src/api/authApi/utils';
import { ObjT } from 'src/utils/types';

export async function signUp(
  userId: string,
  acceptsTerms: boolean,
  termsVersionAccepted: string
) {
  const query = `mutation (
      $email: String!,
      $acceptsTerms: Boolean!,
      $termsVersionAccepted: String!
    ) {
      registerAccount(
        email: $email,
        acceptsTerms: $acceptsTerms,
        termsVersionAccepted: $termsVersionAccepted,
      ) {
        success,
        activationToken,
        errors,
      }
    }`;

  await apiBase.doQuery(
    'signUp',
    query,
    {
      email: userId,
      acceptsTerms,
      termsVersionAccepted,
    },
    (response: ObjT) => {
      if (isError(['registerAccount', 'errors'])(response))
        return {
          success: false,
          errors: [States.SIGN_UP_FAILED],
        };

      return {
        success: true,
        activationToken: response.registerAccount.activationToken,
      };
    },
    (error: ObjT) => {
      return error.response.errors[0].message;
    }
  );
}
