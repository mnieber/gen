# Generate code

## The entry_point loads settings

In the :settings you can define a mapping from :scope~name to :package~names.

## Fn generate_code() reads raw markdown

## Fn generate_code() expands raw markdown

## Fn get_blocks() transforms expanded_markdown to blocks

The {get_blocks.t} adds :lines to each :block.
:It reads the :scope names from the :block name in the {expanded_markdown.t}.
It looks up the :scopes in the {settings.t} and adds them to the :block.

## Fn build_blocks() builds blocks

The {build_blocks.t} creates :relations in each :block.

## Fn process_relations() processes blocks

`Resource creation`

The {process_relations.t} creates :resources for the terms (the subject and object)
in the :relations of each :block. For every :term in a :block B, it tries to find the
resource in the competing:blocks of that :block. If not found, then it determines
the competing:block that describes the :term. In that block, it finds scope that has
the :create-rule for that :term, and runs this :rule. Finally, it adds the created
:resource to the describing :block, and also to the original block B.

`Action creation`

When {process_relations.t} processes a relation in a block B, then it also finds
all matching relation:rules in all :scopes of B. For every matching relation:rule,
it creates an :action. It returns the list with all created :actions.

## Fn run_actions() runs actions

The {run_actions.t} runs the rule of each action in the actions list. Note that
the rule may return "retry", and in that case the action is re-added to the end of the
list. This mechanism helps to run some of the rules in the right order.

## Fn render_resources() renders the root resource to source code

`Rendering template directories`

When a resource is rendered, we iterate over the template directories and render the
templates using the {render_task.render_context.t} and {render_helpers.t}.
The output filename is based on the template filename (with the ".j2" extension
removed), but the {render_meta_data.t} may stipulate a different output filename.
The {render_meta_data.t} may also stipulate that the template is skipped.
The {render_helpers.t} are loaded from the '__moonleap__.py' file in the template
directory.

`The :file-writer`

The {global_file_writer.t} is used to write the rendered files to disk. If the output
is the same as it was in the previous run, then the file-writer may leave the output
file untouched (this is explained in the documentation on syncing the shadow project
with the real project).

`The :rendering-context`

When the resource has been rendered, then the rendering cascade continues with the
:render-tasks that are stored in the resource. In this case, the rendering context
is passed down; in other words, the rendering context gets bigger and bigger as we
descend the rendering cascade. This allows us to use "upstream resources" when rendering
a "down-stream resource". Similarly, the output directory from the upstream resource is
passed down; this means that a downstream resource is rendered in a subdirectory
of the upstream resource.

## Fn post_process_source_code() post-processes the source code

The {post_process_source_code.t} iterates over all files written by the {file_writer.t}.
For every file, it look up the related formatters in the {settings.t} and runs them.

