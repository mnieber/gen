import { fromPairs } from 'ramda';
import { useHistory } from 'react-router-dom';
import { pathname } from '/src/utils/urls';

export interface SearchParamsT {
  get: (name: string) => string | null;
  set: (name: string, value: string) => void;
  all: { [name: string]: string };
}

export const useSearchParams = (): SearchParamsT => {
  const history = useHistory();
  const search_params = new URLSearchParams(window.location.search);

  return {
    get: (name: string) => search_params.get(name),
    set: (name: string, value: string) => {
      if (value === undefined) {
        search_params.delete(name);
      } else {
        search_params.set(name, value);
      }
      const new_url = pathname() + '?' + search_params;
      history.push(new_url);
    },
    all: fromPairs(Array.from(search_params.entries())),
  };
};
