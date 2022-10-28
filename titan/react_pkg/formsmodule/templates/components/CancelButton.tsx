import React from 'react';
import { cn } from 'src/utils/classnames';

interface PropsT {
  onCancel: Function;
  className?: any;
}

export const CancelButton = (props: PropsT) => (
  <button
    className={cn(props.className ?? 'button button--wide', 'ml-2')}
    onClick={(e) => {
      e.preventDefault();
      props.onCancel();
    }}
  >
    cancel
  </button>
);
