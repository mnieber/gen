from titan.react_pkg.reactapp.resources import ReactAppConfig

body = """// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
"""


imports = "import reportWebVitals from './reportWebVitals';"


def get():
    return ReactAppConfig(
        index_body=body,
        index_imports=imports,
    )
