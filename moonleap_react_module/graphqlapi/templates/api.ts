import { always, flow } from 'lodash/fp';
import { doQuery } from 'src/utils/graphqlClient';

{% loop item_list in res.module.store.item_lists %}
export function get{{ item_list.plural_item_name|title }}() {
  const query = `query query{{ item_list.plural_item_name|title }} {
    {{ item_list.plural_item_name }} {
      {{ item_list.item_name }} {
        uuid
        name
      }
    }
  }`;
  const vars = {};
  return doQuery(query, vars).then((response) => {
    return {
      {{ item_list.plural_item_name }}: flow(
        always(response.{{ item_list.plural_item_name }}),
      )(),
    };
  });
}
{% endloop %}
