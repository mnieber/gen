from moonleap.utils.magic_replace import magic_replace

construct_item_list_template = """
  @observable yellowTulipById: YellowTulipByIdT = listToItemById(gardenFlowersConstants.yellowTulips);
"""  # noqa

import_api_template = """
import * as gardenFlowersConstants from 'src/gardenFlowers/api';
import { listToItemById } from 'src/utils/ids';
"""


def construct_item_list_section(self, item_list):
    return magic_replace(
        construct_item_list_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )


def import_api_section(self):
    return magic_replace(
        import_api_template,
        [("gardenFlowers", self.module.name)],
    )
