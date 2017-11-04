__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

YES_LABEL = 'y'
NO_LABEL = 'n'

class Parser:
    def __init__(self, yes_data_filepath, no_data_filepath):
        self.yes_data_filepath = yes_data_filepath
        self.no_data_filepath = no_data_filepath
        self.item_size = (25, 10)

    def items(self):
        height, _ = self.item_size
        with open(self.yes_data_filepath, 'r') as data_file:
            items = []
            spectogram = []
            for index, line in enumerate(data_file):
                spectogram.append(list(line.replace('\n', '')))
                if index % height == height - 1:
                    yield (spectogram, YES_LABEL)
                    spectogram = []

                    data_file.readline()
                    data_file.readline()
                    data_file.readline()

        with open(self.no_data_filepath, 'r') as data_file:
            items = []
            spectogram = []
            for index, line in enumerate(data_file):
                spectogram.append(list(line.replace('\n', '')))
                if index % height == height - 1:
                    data_file.readline()
                    data_file.readline()
                    data_file.readline()

                    yield (spectogram, NO_LABEL)
                    spectogram = []

if __name__ == '__main__':
    height = 25
    width = 10
    parser = Parser('part1data/yes_train.txt', 'part1data/no_train.txt')

    count = 0
    for item in parser.items():
        count += 1
        
        assert type(item) == tuple

        # check first item in the tuple is our matrix (list of lists)
        assert type(item[ 0 ]) == list

        # check label is an int
        assert type(item[ 1 ]) == str
        assert item[ 1 ] == YES_LABEL or item[ 1 ] == NO_LABEL

        # check number of rows is right
        assert len(item[ 0 ]) == height

        # check number of columns is right
        assert len(item[ 0 ][ 0 ]) == width

    assert count == 271
