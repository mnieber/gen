import Cookies from 'js-cookie';

export function maybeSetCypressCookie(name: string, value: string) {
  if (import.meta.env.VITE_ADD_COOKIES_FOR_CYPRESS?.toLowerCase() === 'true') {
    Cookies.set(name, value);
  }
}
