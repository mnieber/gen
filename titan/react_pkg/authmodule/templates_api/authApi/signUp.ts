import { States } from 'src/api/authApi/states';
import { isError } from 'src/api/authApi/utils';
import { doQuery } from 'src/utils/graphqlClient';
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
  const response: ObjT = await doQuery(query, {
    email: userId,
    acceptsTerms,
    termsVersionAccepted,
  });

  if (isError(['registerAccount', 'errors'])(response))
    return {
      success: false,
      errors: [States.SIGN_UP_FAILED],
    };

  return {
    success: true,
    activationToken: response.registerAccount.activationToken,
  };
}
