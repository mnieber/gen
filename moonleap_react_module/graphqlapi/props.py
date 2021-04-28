from moonleap.utils.magic_replace import magic_replace

construct_item_list_template = """
  @observable yellowTulipById: YellowTulipByIdT = {};
  @observable yellowTulipByIdRS: RST = resetRS();
"""

load_item_list_template = """
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
"""

save_list_item_template = """
  @action saveYellowTulip = (values: any) => {
    gardenFlowersApi.saveYellowTulip(values);
  }
"""


def construct_item_list_section(self, item_list):
    return magic_replace(
        construct_item_list_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )


def load_item_list_section(self, item_list):
    return magic_replace(
        load_item_list_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )


def save_list_item_section(self, item_list):
    return magic_replace(
        save_list_item_template,
        [("gardenFlowers", self.module.name), ("yellowTulip", item_list.item_name)],
    )
