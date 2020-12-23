from parser import Block


class Config:
    def __init__(self):
        self.blocks = [Block("global")]

    @property
    def global_block(self):
        return self.blocks[0]


config = Config()
