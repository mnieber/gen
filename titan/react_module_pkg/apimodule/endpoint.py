import os

import ramda as R
from moonleap import chop0
from moonleap.resources.type_spec_store import (
    flattened_spec_field_by_name,
    type_spec_store,
)
from moonleap.utils.fp import ds
from moonleap.utils.inflect import plural
from moonleap.utils.magic_replace import magic_replace

endpoint_template = chop0(
    """
  endpointName(
    javaScriptArgs
  ) {
    return this._doQuery(
      'endpointName',
      `graphqlHeader{
        endpointName(
          redRose
        ) {
          graphqlBody
        }
      }`,
      {
          blueDaisy
      },
      (response: ObjT) => purpleOrchid,
      (error: ObjT) => error.response.errors[0].message
    );
  }
"""
)


def _javascript_args(type_spec):
    field_specs = flattened_spec_field_by_name(type_spec).items()
    return ", ".join(R.map(ds(_field_spec_to_ts_arg), field_specs))


def _graphql_header(type_spec, name, query_type):
    field_specs = flattened_spec_field_by_name(type_spec).items()
    return (os.linesep + " " * 6).join(
        [
            f"{query_type} {name}" + ("(" if field_specs else ""),
            *map(ds(lambda n, t: "  " + _field_spec_to_graphql_arg(n, t)), field_specs),
            ") " if field_specs else "",
        ]
    )


def _graphql_body(type_spec, indent=0, skip=None):
    if skip is None:
        skip = [type_spec.type_name]

    graphqlBody = []
    for spec_field in flattened_spec_field_by_name(type_spec).values():
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = spec_field.field_type_attrs["target"]
            if fk_type_name not in skip:
                fk_type_spec = type_spec_store().get(fk_type_name)
                graphqlBody.append(f"{spec_field.name} {{")
                graphqlBody.extend(
                    _graphql_body(
                        fk_type_spec,
                        indent + 2,
                        skip + [fk_type_name],
                    )
                )
                graphqlBody.append(f"}}")  # noqa: F541
        else:
            graphqlBody.append(f"{spec_field.name}")

    if indent == 0:
        return (os.linesep + (" " * 10)).join(graphqlBody)
    else:
        return [(" " * indent) + x for x in graphqlBody]


def get_endpoint_query_text(query):
    field_names = flattened_spec_field_by_name(query.inputs_type_spec).keys()

    return magic_replace(
        endpoint_template,
        [
            ("endpointName", query.name),
            (
                "javaScriptArgs",
                _javascript_args(query.inputs_type_spec),
            ),
            (
                "graphqlHeader",
                _graphql_header(query.inputs_type_spec, query.name, "query"),
            ),
            (
                "redRose",
                (os.linesep + " " * 8).join(map(lambda x: f"{x}: ${x}", field_names)),
            ),
            (
                "graphqlBody",
                _graphql_body(query.outputs_type_spec),
            ),
            ("blueDaisy", ("," + os.linesep + " " * 8).join(field_names)),
            ("purpleOrchid", get_graphql_response(query, is_list=True)),
        ],
    )


def get_endpoint_mutation_text(mutation):
    return magic_replace(
        endpoint_template,
        [
            ("endpointName", mutation.name),
            (
                "javaScriptArgs",
                _javascript_args(mutation.inputs_type_spec),
            ),
            (
                "graphqlHeader",
                _graphql_header(mutation.inputs_type_spec, mutation.name, "mutation"),
            ),
            (
                "graphqlBody",
                _graphql_body(mutation.outputs_type_spec),
            ),
        ],
    )


def get_graphql_response(query, is_list):
    if is_list:
        return (
            f"normalize(response.{plural(query.name)}, {plural(query.name)}).entities"
        )
    else:
        return f"normalize(response.{query.name}, {query.name}).entities"
