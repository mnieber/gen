import classnames from 'classnames';

export const cn = (...args: any[]) => {
  return classnames(...args);
};

export const d = (label: string) => {
  return import.meta.env.PROD && label.endsWith('__') ? undefined : label;
};
