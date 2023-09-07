import { useFieldProps } from '/src/forms/hooks';
import { cn } from '/src/utils/classnames';

// Import styles
import './ControlledCheckbox.scss';

type PropsT = {};

export const ControlledCheckbox = (props: PropsT) => {
  const fieldProps = useFieldProps({
    fieldType: 'checkbox',
  });

  return (
    <div className={cn('ControlledCheckbox', 'flex flex-row')}>
      <input className="py-2" {...fieldProps} />
    </div>
  );
};
