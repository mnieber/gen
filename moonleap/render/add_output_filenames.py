def add_output_filenames(all_output_filenames, x):
    if not isinstance(x, list):
        raise Exception(
            "The render() function should return a list of output filenames"
        )
    all_output_filenames += x
