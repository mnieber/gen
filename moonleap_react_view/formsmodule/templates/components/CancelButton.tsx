import React from 'react';
import classnames from 'classnames';

interface PropsT {
  onCancel: Function;
  className?: string;
}

export const CancelButton: React.FC<PropsT> = (props: PropsT) => (
  <button
    className={classnames(props.className ?? 'button button--wide', 'ml-2')}
    onClick={(e) => {
      e.preventDefault();
      props.onCancel();
    }}
  >
    cancel
  </button>
);
