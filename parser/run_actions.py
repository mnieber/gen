def run_actions(blocks, actions):
    __import__("pudb").set_trace()
    for block in blocks:
        for line in block.lines:
            for tags, action in actions.items():
                terms = [line.find_terms(tags)]
                if None not in terms:
                    action(*terms, line, block)
