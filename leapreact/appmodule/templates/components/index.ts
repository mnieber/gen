{% for component in res.components %}
import { {{ component.name }} } from "./{{ component.name }}.tsx"
{% endfor %}