import TextareaAutosize from 'react-textarea-autosize';
import { useFieldProps, type FieldPropsT } from 'src/forms/hooks';
import { cn } from 'src/utils/classnames';
import './TextAreaField.scss';

type PropsT = Partial<FieldPropsT> & {
  className?: any;
};

export const TextAreaField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    ...props,
    fieldType: props.fieldType ?? 'text',
  });

  return (
    <div className={cn('TextAreaField', props.className)}>
      <TextareaAutosize type="text" {...(fieldProps as any)} />
    </div>
  );
};
