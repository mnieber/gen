from moonleap import upper0


def item_list_and_api_pairs(self):
    result = []
    for api in self.module.apis:
        for item_list in self.item_lists:
            if api.provides_item_list(item_list):
                result.append((item_list, api))
    return result


def apis(self):
    result = []
    for api in self.module.apis:
        for item_list in self.item_lists:
            if api.provides_item_list(item_list) and api not in result:
                result.append(api)
    return result


def construct_item_lists_section(self):
    result = ""
    for item_list in self.item_lists:
        line = ""
        for api in self.module.apis:
            if api.provides_item_list(item_list):
                line = api.construct_item_list_section(item_list)
                break
        if not line:
            line = (
                f"  {item_list.item_name}ById: "
                + f"{upper0(item_list.item_name)}ByIdT = {{}};\n"
            )
        result += line
    return result
