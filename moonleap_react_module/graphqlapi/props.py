from moonleap.utils.magic_replace import magic_replace

import_api_template = """
import { action, observable, makeObservable } from 'mobx';
import { RST, resetRS, updateRes } from 'src/utils/RST';
import { forEach } from 'lodash/fp';
import * from 'src/gardenFlowers/api' as gardenFlowersApi;
"""

construct_item_list_template = """
  @observable yellowTulipById: YellowTulipByIdT = {};
  @observable yellowTulipByIdRS: RST = resetRS();
"""

item_list_io_template = """
  @action loadYellowTulips = () => {
    updateRes(
      this,
      'yellowTulipByIdRS',
      () => {
        return gardenFlowersApi.getYellowTulips();
      },
      (response: any) => {
        this.addYellowTulips(response.yellowTulips);
      },
      (message: any) => {
        console.log(message);
        return 'Oops, there was an error getting the yellowTulips data';
      }
    );
  }

  @action saveYellowTulip = (values: any) => {
    gardenFlowersApi.saveYellowTulip(values);
  }

  @action addYellowTulips = (yellowTulips: YellowTulipT[]) => {
    forEach((yellowTulip: YellowTulipT) => {
      this.yellowTulipById[yellowTulip.id] = yellowTulip;
    }, yellowTulips);
  }
"""


def construct_item_list_section(self, item_list):
    return magic_replace(
        construct_item_list_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )


def item_list_io_section(self, item_list):
    return magic_replace(
        item_list_io_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )


def import_api_section(self):
    return magic_replace(
        import_api_template,
        [("gardenFlowers", self.module.name)],
    )
