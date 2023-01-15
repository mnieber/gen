def add_tpl_to_builder(tpl, builder):
    imports = tpl.get_section("imports")
    props = tpl.get_section("props")
    add_props = tpl.get_section("add_props")
    scss = tpl.get_section("scss")
    preamble = tpl.get_section("preamble")
    preamble_hooks = tpl.get_section("preamble_hooks")
    lines = tpl.get_section("lines")

    builder.output.add(
        imports=[imports] if imports else None,
        preamble=[preamble] if preamble else None,
        preamble_hooks=[preamble_hooks] if preamble_hooks else None,
        lines=[lines] if lines else None,
        props=[props] if props else None,
        add_props=[add_props] if add_props else None,
        scss=[scss] if scss else None,
    )
