import os


def policy_lines(store):
    result = []
    return os.linesep.join(result)


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
