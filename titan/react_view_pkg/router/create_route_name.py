_route_nr = 0


def create_route_name():
    global _route_nr
    _route_nr += 1
    return f"route_{_route_nr}"
