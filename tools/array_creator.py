"""
Tool used to create blank 2D array level structure with pre-made edges.
Useful for making levels of various sizes before adding tiles.
"""

class ArrayCreator:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.edge = 0
        self.empty = 0
        self.full = 0

        self.block = []
        self.open = []

    def main(self) -> None:
        for i in range(5):
            self.query(i)
        self.create_block()
        self.create_open()
        self.create_array()

    def query(self, number: int) -> None:
        """Attain user input without looping
        all queries in case of error."""
        error = ''
        while True:
            try:
                if number == 0:
                    width = int(input('Array width: '))
                    if width > 0:
                        self.width = width
                        return
                    else:
                        error = 'negative'
                elif number == 1:
                    height = int(input('Array height: '))
                    if height > 0:
                        self.height = height
                        return
                    else:
                        error = 'negative'
                elif number == 2:
                    edge = int(input('Thickness of edges: '))
                    if edge >= 0:
                        if edge < self.width // 2 and edge < self.height // 2:
                            self.edge = edge
                            return
                        else:
                            error = 'edge'
                    else:
                        error = 'negative'
                elif number == 3:
                    full = int(input('Value representing full tiles: '))
                    if full >= 0:
                        self.full = full
                        return
                    else:
                        error = 'negative'
                elif number == 4:
                    empty = int(input('Value representing empty tiles: '))
                    if empty >= 0:
                        self.empty = empty
                        return
                    else:
                        error = 'negative'
                if error == 'edge':
                    print('The edge must be at least half the width and height of the array.')
                elif error == 'negative':
                    print('Value must be positive.')
            except ValueError:
                print('Please enter digits only, eg. 0 or 5.')

    def create_block(self) -> None:
        """Creates a list with full tiles
        for the top and bottom layers of the level."""
        for _ in range(self.width):
            self.block.append(self.full)

    def create_open(self) -> None:
        """Creates a list with full tiles in on the edges
        while the centre is filled with empty tiles."""
        for i in range (self.width):
            if i < self.edge:
                self.open.append(self.full)
            elif self.width - self.edge > i >= self.edge:
                self.open.append(self.empty)
            elif i >= self.width - self.edge:
                self.open.append(self.full)

    def create_array(self) -> None:
        """Saves an array similar to the structure of the 2D numpy array."""
        with open('level_.txt', 'w') as f:
            f.write('[\n')
            for i in range(self.height):
                if i < self.edge:
                    row = self.block
                elif self.height - self.edge > i >= self.edge:
                    row = self.open
                elif i >= self.height - self.edge:
                    row = self.block
                f.write(str(row) + ',\n')
            f.write(']')
        print('Array was saved as "level_.txt".')


if __name__ == '__main__':
    creator = ArrayCreator()
    creator.main()