import ramda as R


def uppercase_dict_keys(x):
    return R.pipe(
        R.always(x),
        R.to_pairs,
        R.map(lambda x: (x[0].upper(), x[1])),
        R.sort_by(lambda x: x[0]),
        R.from_pairs,
    )(None)
