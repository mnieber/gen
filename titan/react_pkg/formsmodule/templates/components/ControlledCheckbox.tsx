import { useFieldProps } from 'src/forms/hooks';
import { cn } from 'src/utils/classnames';
import './ControlledCheckbox.scss';

type PropsT = {};

export const ControlledCheckbox = (props: PropsT) => {
  const fieldProps = useFieldProps({
    fieldType: 'checkbox',
  });

  return (
    <input
      className={cn('ControlledCheckbox', 'text-primary')}
      {...fieldProps}
    />
  );
};
