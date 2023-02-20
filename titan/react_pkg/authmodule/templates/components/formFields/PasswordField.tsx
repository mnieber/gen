import { useFieldProps } from 'src/forms/hooks';

type PropsT = { placeholder: string; className?: any };

export const PasswordField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    fieldType: 'password',
    placeholder: props.placeholder,
    autoSelect: true,
  });

  return <input className={props.className} {...fieldProps} />;
};
