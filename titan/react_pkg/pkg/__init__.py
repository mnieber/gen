from moonleap.render.simple_file_merger import SimpleFileMerger

from . import jsfilemerger

SimpleFileMerger.add_patterns(["index.scss", ".gitignore"])

file_mergers = [jsfilemerger.JsFileMerger(), SimpleFileMerger()]
