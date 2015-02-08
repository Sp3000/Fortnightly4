class InvalidCommandException(Exception):
    pass

class Block():
    def __init__(self, x, y, data):
        self.block = x+y*1j
        self.data = data

    def __getattr__(self, name):
        return getattr(self.block, name)

    def __repr__(self):
        return repr(self.block)
    
class BlockStructure():
    def __init__(self):
        self.blocks = {} # blocks : [connected neighbours]
        self.obj_dict = {} # complex : block

    def place(self, x, y, colour):
        block_c = x+y*1j
        
        if block_c in self.obj_dict:
            raise InvalidCommandException

        new_block = Block(x, y, colour)
        self.obj_dict[block_c] = new_block        
        self.blocks[new_block] = set()

    def remove(self, x, y):
        block_c = x+y*1j
        
        if block_c not in self.obj_dict:
            raise InvalidCommandException

        block = self.obj_dict[block_c]

        for neighbour in self.blocks[block]:
            self.blocks[neighbour].remove(block)
            
        del self.blocks[block]
        del self.obj_dict[block_c]

    def connect(self, x1, y1, x2, y2):
        block_c1 = x1+y1*1j
        block_c2 = x2+y2*1j

        if block_c1 not in self.obj_dict or block_c2 not in self.obj_dict:
            raise InvalidCommandException

        if abs(block_c1 - block_c2) != 1:
            raise InvalidCommandException

        block1 = self.obj_dict[block_c1]
        block2 = self.obj_dict[block_c2]

        if block1 in self.blocks[block2]:            
            raise InvalidCommandException

        self.blocks[block1].add(block2)
        self.blocks[block2].add(block1)

    def disconnect(self, x1, y1, x2, y2):
        block_c1 = x1+y1*1j
        block_c2 = x2+y2*1j
        
        if block_c1 not in self.obj_dict or block_c2 not in self.obj_dict:
            raise InvalidCommandException

        if abs(block_c1 - block_c2) != 1:
            raise InvalidCommandException

        block1 = self.obj_dict[block_c1]
        block2 = self.obj_dict[block_c2]

        if block1 not in self.blocks[block2]:            
            raise InvalidCommandException

        self.blocks[block1].remove(block2)
        self.blocks[block2].remove(block1)

    def count(self):
        all_blocks = set(self.blocks.keys())
        n_structures = 0
        
        while all_blocks:
            start_block = all_blocks.pop()
            n_structures += 1
            all_blocks -= self._flood_fill(start_block)

        return n_structures

    def move(self, x, y, dx, dy):
        block_c = x+y*1j

        if block_c not in self.obj_dict:
            raise InvalidCommandException

        block = self.obj_dict[block_c]
        structure = self._flood_fill(block)
        
        delta = dx+dy*1j
        curr_positions = {block.block for block in structure}

        if any(block.block + delta not in curr_positions and
               block.block + delta in set(self.obj_dict.keys())
               for block in structure):
               
            raise InvalidCommandException
        
        for block in structure:
            del self.obj_dict[block.block]
            block.block += delta
            self.obj_dict[block.block] = block

    def rotate(self, x, y, cw_times):
        block_c = x+y*1j

        if block_c not in self.obj_dict:
            raise InvalidCommandException

        block = self.obj_dict[block_c]
        structure = self._flood_fill(block)

        transform = lambda pos: (pos - block_c)*((-1j)**cw_times) + block_c
        curr_positions = {block.block for block in structure}

        if any(transform(block.block) not in curr_positions and
               transform(block.block) in set(self.obj_dict.keys())
               for block in structure):
            
            raise InvalidCommandException

        for block in structure:
            del self.obj_dict[block.block]
            block.block = transform(block.block)
            self.obj_dict[block.block] = block

    def connected(self, x1, y1, x2, y2):
        block_c1 = x1+y1*1j
        block_c2 = x2+y2*1j
        
        if block_c1 not in self.obj_dict or block_c2 not in self.obj_dict:
            return False

        block1 = self.obj_dict[block_c1]
        structure = self._flood_fill(block1)

        return (self.obj_dict[block_c2] in structure)

    def nearest(self, x, y):
        if not self.blocks:
            raise InvalidCommandException
        
        min_ = min(abs(block.block.real - x) + abs(block.block.imag - y) for block in self.blocks.keys())

        return [(int(block.block.real), int(block.block.imag), block.data) for block in self.blocks.keys()
                if abs(block.block.real - x) + abs(block.block.imag - y) == min_]


    def colour(self, colour):
        return [block for block in self.blocks if block.data == colour]
    
                
    def _flood_fill(self, block):        
        connected = {block}
        to_search = [block]

        while to_search:
            curr_block = to_search.pop()
            
            for neighbour in self.blocks[curr_block]:
                if neighbour not in connected:
                    connected.add(neighbour)
                    to_search.append(neighbour)

        return connected

    def __repr__(self):
        return repr(self.blocks)
