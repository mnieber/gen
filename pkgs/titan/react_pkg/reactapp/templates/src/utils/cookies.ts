import Cookies from 'js-cookie';

export function maybeSetCypressCookie(name: string, value: string) {
  if (process.env.REACT_APP_ADD_COOKIES_FOR_CYPRESS?.toLowerCase() === 'true') {
    Cookies.set(name, value);
  }
}
