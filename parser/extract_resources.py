#


def extract_resources(global_block, global_tags, blocks, builders):
    for block in blocks:
        for line in block.lines:
            new_resource_by_term = {}
            for term in line.terms:
                builder = builders.get(term.tag)
                if not builder:
                    continue

                is_global = term.tag in global_tags
                target_block = global_block if is_global else block
                if term in target_block.resource_by_term:
                    continue

                resource = builder.create(term, line, block)
                target_block.add_resource(resource, term)
                new_resource_by_term[term] = resource

            for term, resource in new_resource_by_term.items():
                builder = builders.get(term.tag)
                if hasattr(builder, "build"):
                    builder.build(resource, term, line, block)
