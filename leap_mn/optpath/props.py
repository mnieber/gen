import ramda as R


def select_all_opt_paths(self):
    chain = R.chain(R.identity)
    return chain([x.opt_paths for x in self.opt_path_sources])
