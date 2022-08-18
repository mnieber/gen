import { useFieldProps } from 'src/forms/hooks';

type PropsT = {
  className?: any;
};

export const EmailField = (props: PropsT) => {
  const fieldProps = useFieldProps({ fieldType: 'text' });

  return <input className={props.className} {...fieldProps} />;
};
