# Glossary

**block**: a section of the spec file
**block body**: the text of the block section
**block section**: the section of the spec file that the block corresponds to
**block scope**: a label that is added to a block to indicate which scope it belongs to (e.g. backend, frontend, database, etc). Every scope has associated creation rules and relation rules
**block title**: the heading of the block section
**creation rule**: a rule that turns a term into a resource
**external link**: a link to an external spec file that is included into
the spec file
**relation rule**: a rule that updates existing resources that are in a certain relationship
**spec dir**: the directory that contains the spec file
**spec file**: the root markdown file that contains the project specification
**term**: a word in the spec that contains - or is prefixed by - a colon. The part before the colon is called 'data' and the part after
is called 'tag'.
**verb**: a word in the spec that is prefixed with a forward slash

# Purpose

Moonleap turns a markdown-based spec file into a set of source files.

# Steps

## Expanding the spec file

1.0 When this step finds an external links in the block title, it
replaces the block body with the contents of the linked file.
1.1 ..In this case, it adds the name of the external file as a scope
to the block
2.0 The expanded spec file is saved to the moonleap dir.

# Parsing

1.0 Every block is split into lines, that are split into terms.
1.1 ..A repeated colon is ignored for creating terms (e.g. foo::bar)
2.0 The terms :It and :it have a special meaning. They refer back to the first term in the previous sentence.
