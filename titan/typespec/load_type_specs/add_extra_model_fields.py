from moonleap import l0

from .foreign_key import ForeignKey


def add_extra_model_fields(type_spec, value, fk: ForeignKey, parent_type_spec=None):
    # Add an auto-field for the entity id
    if (
        type_spec.is_entity
        and not type_spec.get_field_spec_by_key("id")
        and not value.get("id")
    ):
        value["id"] = "Id,primary_key,auto"

    # Add an auto-field for the sortPos
    if (
        type_spec.is_sorted
        and not type_spec.get_field_spec_by_key("sortPos")
        and not value.get("sortPos")
    ):
        value["sortPos|"] = "Int = 0"

    # If we are adding a related set, then create a related fk auto-field that points back
    # to the parent type-spec. Note that this auto-field may be added to the type spec and then
    # removed again if some non-auto field is using the same name.
    if fk.field_type == "relatedSet" and parent_type_spec:
        # Below we show an example of how the auto-field is added to the type spec. Note that
        # the with-clause specifies the related_name of the RelatedSet.
        #
        # userProfile:
        #   playlistSet: pass
        #   myPlaylists as playlistSet with owner: pass
        #
        # to
        #
        # userProfile:
        #   playlistSet: pass
        #     userProfile with playlistSet: pass
        #   myPlaylists as playlistSet with owner: pass
        #     owner as userProfile with myPlaylistSet: pass
        fk_field_name = l0(parent_type_spec.type_name)

        if fk.related_name:
            fk_field_name = f"{fk.related_name} as {fk_field_name}"

        key = fk_field_name + f" with {fk.var}"
        if key not in value:
            required = "is_owner" in fk.parts
            value[key] = "pass,auto" + ("" if required else ",optional")
