def has_pkg(self, pkg_name):
    for pkg in self.pkgs:
        if pkg.name == pkg_name:
            return True
    return False
