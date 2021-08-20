import React from 'react';
import classnames from 'classnames';
import { Link } from 'react-router-dom';

type PropsT = React.PropsWithChildren<{
  to: string;
  className?: any;
  dataCy?: string;
  onClick?: (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
}>;

export const RouterLink: React.FC<PropsT> = (props: PropsT) => {
  return (
    <Link
      data-cy={props.dataCy}
      className={classnames(props.className)}
      to={props.to}
      onClick={props.onClick}
    >
      {props.children}
    </Link>
  );
};
