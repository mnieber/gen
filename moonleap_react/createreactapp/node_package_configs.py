from moonleap_react.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "@testing-library/jest-dom": "^5.11.4",
                "@testing-library/react": "^11.1.0",
                "@testing-library/user-event": "^12.1.10",
                "@types/jest": "^26.0.15",
                "@types/node": "^12.0.0",
                "@types/react": "^17.0.0",
                "@types/react-dom": "^17.0.0",
                "react": "^17.0.1",
                "react-dom": "^17.0.1",
                "react-scripts": "4.0.2",
                "typescript": "^4.1.2",
                "web-vitals": "^1.0.1",
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject",
            },
            "eslintConfig": {"extends": ["react-app", "react-app/jest"]},
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version",
                ],
            },
        }
    )
