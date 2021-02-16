import { always, flow, map, values } from 'lodash/fp';
import { observer } from 'mobx-react-lite';
import { useStore } from 'src/app/StoreProvider';

export const {{ res.name }} = observer(() => {
  const { {{ res.item_name|store }} } = useStore();

  const {{ res.item_name }}Divs = flow(
    always({{ res.item_name|store }}.{{ res.item_name|byId }}),
    values,
    map((x) => (
      <{{ res.name }}Item
        key={x.uuid}
        {{ res.item_name }}={x}
      />
    ))
  )();

  const noItems = <h2>There are no {{ res.item_name|plural }}</h2>;

  const updatedDiv = (
    <div className="{{ res.name }} flex flex-col w-full">
      { {{ res.item_name }}Divs.length && {{ res.item_name }}Divs }
      {!{{ res.item_name }}Divs.length && noItems}
    </div>
  );

  return (
    <ResourceView
      rs={ {{ res.item_name|store }}.{{ res.item_name|byId }} }
      renderUpdated={() => updatedDiv}
      renderErrored={(message) => {
        return <div className="text-white">{message}</div>;
      }}
    />
  );
}
