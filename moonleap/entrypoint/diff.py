import ramda as R
from plumbum import local


def _diff_tool_name_and_exe(settings):
    diff_tool_name = settings.get("diff_tool", "diff")
    return diff_tool_name, R.path_or(diff_tool_name, ["bin", diff_tool_name, "exe"])(
        settings
    )


def _diff(session, from_dir, to_dir, sudo=False):
    diff_tool_name, diff_tool_exe = _diff_tool_name_and_exe(session.settings)
    if diff_tool_name == "meld":
        args = [diff_tool_exe, from_dir, to_dir]
    else:
        session.report(f"Unknown diff tool: {diff_tool_name}")
        return

    if sudo:
        args.insert(0, "sudo")
    local[args[0]](*args[1:])


def diff(session, sudo=False):
    _diff(session, ".moonleap/output", session.expected_dir, sudo)
