from moonleap.parser.block import has_terms_in_same_line


def update(block, git_repo_term, src_dir_term):
    if has_terms_in_same_line(block, git_repo_term, src_dir_term, is_ordered=False):
        git_repo = block.get_resource(git_repo_term)
        src_dir = block.get_resource(src_dir_term)
        src_dir.git_repo = git_repo
        block.drop_resource_by_term(git_repo_term)
