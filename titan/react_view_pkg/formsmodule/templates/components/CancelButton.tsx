import classnames from 'classnames';
import React from 'react';

interface PropsT {
  onCancel: Function;
  className?: any;
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
