import ramda as R
from titan.api_pkg.pkg.ml_name import ml_form_type_spec_from_item_name


def get_context(form_view):
    _ = lambda: None
    _.form_type_spec = ml_form_type_spec_from_item_name(form_view.item_posted.item_name)
    _.form_field_specs = [x for x in _.form_type_spec.field_specs if x.name != "id"]

    _.mutation = R.head(form_view.item_posted.poster_mutations)
    _.postmethod = _.mutation.name

    class Sections:
        pass

    return dict(sections=Sections(), _=_)
