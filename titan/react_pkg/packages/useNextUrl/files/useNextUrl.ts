import React from 'react';
import { useHistory } from 'react-router-dom';

export const searchParams = () => new URLSearchParams(window.location.search);

export const getNextUrl = (defaultUrl: string) =>
  searchParams().get('next') ?? defaultUrl;

// This effect browses to url if it's defined
export const useNextUrl = (url: string | undefined) => {
  const history = useHistory();
  React.useEffect(() => {
    if (url) {
      if (url.startsWith('http://') || url.startsWith('https://')) {
        // @ts-ignore
        window.location = url;
      } else {
        history.push(url);
      }
    }
  }, [url, history]);
};
