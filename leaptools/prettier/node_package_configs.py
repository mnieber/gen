from leaptools.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "devDependencies": {
                "prettier": "2.0.5",
            },
            "scripts": {
                "prettier-all": "yarn prettier --list-different '**/*.js' '**/*.jsx'",
                "prettier-all-save": "yarn prettier --write '**/*.js' '**/*.jsx'",
            },
        }
    )
