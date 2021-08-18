import React from 'react';
import { useHistory } from 'react-router-dom';

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
