import random

from blockstructure import BlockStructure


class TestGenerator():
    def __init__(self):
        self.structure = BlockStructure()

        self.has_block_neighbour = set()
        self.has_empty_neighbour = set()
