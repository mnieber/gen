import { flags } from '/src/app/flags';

export const joinUrls = (lhs: string, rhs: string) => {
  if (lhs.endsWith('/') && rhs.startsWith('/')) {
    return lhs + rhs.substring(1);
  } else if (!lhs.endsWith('/') && !rhs.startsWith('/')) {
    return lhs + '/' + rhs;
  } else {
    return lhs + rhs;
  }
};

export const pathname = () => {
  const result = window.location.pathname;
  return chopTrailingSlash(result);
};

export function chopTrailingSlash(result: string) {
  return result.endsWith('/') ? result.slice(0, result.length - 1) : result;
}

export function patchHistory(history: any) {
  var push = history.push;
  history.push = function (state: any) {
    if (typeof history.onpush == 'function') {
      history.onpush({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.push', arguments[0]);
    }
    return push.apply(history, arguments);
  };

  var replace = history.replace;
  history.replace = function (state: any) {
    if (typeof history.onreplace == 'function') {
      history.onreplace({ state: state });
    }
    if (flags.logHistory) {
      console.log('history.replace', arguments[0]);
    }
    return replace.apply(history, arguments);
  };
  return history;
}
