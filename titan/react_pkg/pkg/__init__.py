from moonleap.render.file_merger import simplefilemerger

from . import jsfilemerger

simplefilemerger.SimpleFileMerger.add_patterns(["index.scss", ".gitignore"])

file_mergers = [jsfilemerger.JsFileMerger(), simplefilemerger.SimpleFileMerger()]
