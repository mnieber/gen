def view_collapses(panel):
    return panel.module.react_app.service.get_tweak_or(
        True,
        [
            "react_app",
            "components",
            panel.name,
            "collapses",
        ],
    )
