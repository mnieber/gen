from titan.react_pkg.reactapp import ReactAppConfig

imports = """import { toJS } from 'mobx';
import { setOptions } from 'skandha';
import { flags } from 'src/app/flags';
"""

body = """setOptions({
  logging: flags.logSkandha,
  formatObject: toJS,
});
"""


config = ReactAppConfig(
    flags={"logSkandha": False}, index_imports=imports, index_body=body
)
