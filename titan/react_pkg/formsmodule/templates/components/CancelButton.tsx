import React from 'react';
import { button } from 'src/frames/components';

interface PropsT {
  onCancel: Function;
  className?: any;
}

export const CancelButton = (props: PropsT) => (
  <button
    className={props.className ?? `${button} ml-2`}
    onClick={(e) => {
      e.preventDefault();
      props.onCancel();
    }}
  >
    cancel
  </button>
);
