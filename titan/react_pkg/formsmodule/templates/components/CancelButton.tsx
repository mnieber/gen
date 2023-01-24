import { useFormStateContext } from 'react-form-state-context';
import { button } from 'src/frames/components';
import { cn } from 'src/utils/classnames';

export type PropsT = {
  label: string;
  disabled?: boolean;
  className?: any;
  useDefaultClassName?: boolean;
};

export const CancelButton = (props: PropsT) => {
  const formState = useFormStateContext();

  return (
    <button
      className={cn(
        (props.useDefaultClassName ?? true) && [button, `!mr-2`],
        props.className
      )}
      onClick={(e) => {
        e.preventDefault();
        formState.cancel();
      }}
      disabled={props.disabled || formState.getFlag('submitting')}
    >
      {props.label}
    </button>
  );
};
