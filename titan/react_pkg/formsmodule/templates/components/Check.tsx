import { cn } from '/src/utils/classnames';

// Import styles
import './Check.scss';

type PropsT = {
  value: boolean;
  className?: any;
};

export const Check = (props: PropsT) => {
  return (
    <input
      className={cn(
        'FilterComboItem__Check text-primary',
        {
          'FilterComboItem__Check--checked': props.value,
        },
        props.className
      )}
      type="checkbox"
      readOnly={true}
      checked={props.value}
    />
  );
};
