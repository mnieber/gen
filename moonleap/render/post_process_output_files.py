import re
from collections import defaultdict
from pathlib import Path

from moonleap.utils.fp import append_uniq
from plumbum import local


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def _get_post_process_tools(bin_config):
    result = {}

    prettier = bin_config.get("prettier")
    if prettier:
        prettier_bin = local[prettier["exe"]]
        config = prettier["config"]
        result["prettier"] = lambda fns: prettier_bin(
            ["--config", config, "--write", *fns]
        )

    black = bin_config.get("black")
    if black:
        black_bin = local[black["exe"]]
        result["black"] = lambda fns: black_bin([*fns])

    isort = bin_config.get("isort")
    if isort:
        isort_bin = local[isort["exe"]]
        result["isort"] = lambda fns: isort_bin("--overwrite-in-place", *fns)

    return result


def post_process_output_files(output_filenames, post_process_configs, bin_config):
    tool_by_name = _get_post_process_tools(bin_config)
    fns_by_tool_name = defaultdict(lambda: [])

    for output_fn in output_filenames:
        for suffix_regex, tool_names in post_process_configs.items():
            if re.match(suffix_regex, Path(output_fn).suffix):
                for tool_name in tool_names:
                    append_uniq(fns_by_tool_name[tool_name], output_fn)

    for tool_name, fns in fns_by_tool_name.items():
        tool = tool_by_name.get(tool_name)
        if tool:
            for chunk in chunks(fns, 20):
                tool(chunk)
