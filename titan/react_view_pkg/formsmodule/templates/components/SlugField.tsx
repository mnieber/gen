import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';
import { TextField } from 'src/forms/components/TextField';
import { slugify } from 'src/utils/slugify';

export type PropsT = {
  className?: any;
  relatedFieldName: string;
};

export const UpdateSlugButton = (props: PropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return (
    <div
      className={props.className}
      onClick={() => {
        const newSlug = slugify(formState.values[props.relatedFieldName]);
        if (newSlug) {
          formState.setValue(fieldContext.fieldName, newSlug);
        }
      }}
    >
      Update
    </div>
  );
};

export const SlugField = () => {
  return <TextField className="flex-1" disabled={true} controlled={true} />;
};
