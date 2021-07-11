import os
import re
from collections import defaultdict
from pathlib import Path

from moonleap.settings import get_settings
from plumbum import local


def _get_post_process_tools():
    result = {}
    bin = get_settings().get("bin", {})

    prettier = bin.get("prettier")
    if prettier:
        prettier_bin = local[prettier["exe"]]
        config = prettier["config"]
        result["prettier"] = lambda fns: prettier_bin(
            ["--config", config, "--write", *fns]
        )

    return result


def post_process_output_files(output_filenames):
    tool_by_name = _get_post_process_tools()
    fns_by_tool_name = defaultdict(lambda: [])

    post_process_configs = get_settings().get("post_process", {})
    for output_fn in output_filenames:
        for suffix_regex, tool_names in post_process_configs.items():
            if re.match(suffix_regex, Path(output_fn).suffix):
                for tool_name in tool_names:
                    fns_by_tool_name[tool_name].append(str(output_fn))

    for tool_name, fns in fns_by_tool_name.items():
        tool = tool_by_name.get(tool_name)
        if tool:
            tool(fns)
