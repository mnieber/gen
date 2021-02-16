import { always, flow, map } from 'lodash/fp';
import { observer } from 'mobx-react-lite';
import { useStore } from 'src/app/StoreProvider';

export const {{ res.name }} = observer(() => {
  const { {{ res.plural_item_name }}Store } = useStore();

  const {{ res.item_name }}Divs = flow(
    always({{ res.plural_item_name }}Store.all),
    map((x) => (
      <ExpensesListViewItem
        key={x.uuid}
        expense={x}
      />
    ))
  )();

  const noItems = <h2>There are no expenses</h2>;

  const updatedDiv = (
    <div className="ExpensesListView flex flex-col w-full">
      {expenseDivs.length && expenseDivs}
      {!expenseDivs.length && noItems}
    </div>
  );

  return (
    <ResourceView
      rs={expensesStore.expenseByIdRS}
      renderUpdated={() => updatedDiv}
      renderErrored={(message) => {
        return <div className="text-white">{message}</div>;
      }}
    />
  );
}
