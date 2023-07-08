import { useFieldProps } from '/src/forms/hooks';

type PropsT = {};

export const UsernameField = (props: PropsT) => {
  const fieldProps = useFieldProps({
    fieldType: 'text',
  });

  return <input {...fieldProps} />;
};
