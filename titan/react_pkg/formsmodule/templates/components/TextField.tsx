import { useFieldProps, type FieldPropsT } from 'src/forms/hooks';
import { cn } from 'src/utils/classnames';
import './TextField.scss';

type PropsT = Partial<FieldPropsT> & {
  className?: any;
};

export const TextField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    ...props,
    fieldType: props.fieldType ?? 'text',
  });

  return (
    <div className={cn('TextField', props.className)}>
      <input {...fieldProps} />
    </div>
  );
};
