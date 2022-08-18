import hashlib
import json

from django.conf import settings
from graphql import GraphQLError


def get_query_crc(info):
    body = info.context.body.decode("utf-8")
    query = json.loads(body)["query"].encode("utf-8")
    return hashlib.md5(query).hexdigest()


class GraphqlCheckCRCMiddleware:
    def resolve(self, next, root, info, **kwargs):
        if not info.context.user.has_perm("api.unrestricted_graphql_queries"):
            graphene_settings = getattr(settings, "GRAPHENE", {})
            passlist = graphene_settings.get("APPROVED_QUERY_CRCS", [])
            reveal_crc = graphene_settings.get("REVEAL_REJECTED_QUERY_CRCS", True)
            crc = get_query_crc(info)
            check_crc = getattr(
                graphene_settings, "CHECK_QUERY_CRC", not settings.DEBUG
            )
            if check_crc and crc not in passlist:
                raise GraphQLError(
                    "Unauthorized. You only have permission to execute queries that are "
                    + "on a pass-list. Check the settings.GRAPHQL['APPROVED_QUERY_CRCS'] "
                    + "setting in the server."
                    + (" CRC: " + crc if reveal_crc else "")
                )
        return next(root, info, **kwargs)
