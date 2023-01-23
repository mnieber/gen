from titan.react_view_pkg.pkg.builder import Builder


class ResizeDetectorBuilder(Builder):
    type = "ResizeDetector"

    def build(self):
        self.output.add(
            lines=[tpl],
            imports=["import ReactResizeDetector from 'react-resize-detector';"],
        )
        self.output.set_flags(["app/resizeDetector"])


tpl = """
    <ReactResizeDetector
        handleWidth
        onResize={(width: number) => { console.log("Moonleap Todo"); } }
    />
"""
