from leaptools.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "@craco/craco": "^6.0.0",
                "tailwindcss": "npm:@tailwindcss/postcss7-compat",
            },
            "scripts": {
                "start": "craco start",
                "build": "craco build",
                "test": "craco test",
                "eject": "craco eject",
            },
        }
    )
