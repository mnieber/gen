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
        # is automatically expanded to
        #
        # userProfile:
        #   playlistSet:
        #     userProfile with playlistSet: pass
        #   myPlaylists as playlistSet with owner:
        #     owner as userProfile with myPlaylistSet: pass
        fk_field_name = l0(parent_type_spec.type_name)

        if fk.related_name:
            fk_field_name = f"{fk.related_name} as {fk_field_name}"

        key = fk_field_name + f" with {fk.var}"
        if key not in value:
            required = "is_owner" in fk.parts
            value[key] = "pass,auto" + ("" if required else ",optional")

    # In the case where we add the playlist.userProfile FK, we have to decide whether
    # we want to have a relatedSet pointing from userProfile back to playlist.
    #
    # If no, then we don't have to do anything, the following spec will work:
    #
    # playlist:
    #   owner as userProfile: pass
    #
    # If yes. then we need to add a relatedSet to userProfile:
    #
    # playlist:
    #   owner as userProfile:
    #     playlistSet with owner: pass
    #
    # Note that for this setup to work, you need to specify the related name
    # of the relatedSet (in this case: "owner"). If you forget to do this, then userProfile
    # will end up having two relatedSets pointing back to playlist (because the extra
    # relatedSet to playlist will be unrelated to playlist.owner).
    #
    # Also note that a post-processing step (add_missing_related_names) is used to set the
    # related_name of playlist.owner to "playlistSet" (it's complicated and potentially messy
    # to achieve this by patching the type spec on the fly).

    if fk.field_type == "fk" and parent_type_spec:
        pass
