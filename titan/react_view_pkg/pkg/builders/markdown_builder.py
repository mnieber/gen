from titan.react_view_pkg.pkg.builder import Builder


class MarkdownBuilder(Builder):
    type = "Markdown"

    def build(self):
        text = self.get_value("text") or ""
        self.output.add(
            imports=["import ReactMarkdown from 'react-markdown';"],
            lines=[get_tpl(text)],
        )
        self.output.set_flags(["app/useMarkdown"])


def get_tpl(text):
    return f"""
    <ReactMarkdown>
        {text}
    </ReactMarkdown>
    """


# .Markdown {
#     h1 {
#         @apply text-3xl mb-2;
#     }

#     h2 {
#         @apply text-2xl mb-2;
#     }

#     h3 {
#         @apply text-xl mb-2;
#     }
# }
