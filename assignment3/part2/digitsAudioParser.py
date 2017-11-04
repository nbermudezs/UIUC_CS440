__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

YES_LABEL = 'y'
NO_LABEL = 'n'

class DigitsAudioParser:
    def __init__(self, data_filepath, labels_filepath):
        self.data_filepath = data_filepath
        self.labels_filepath = labels_filepath
        self.item_size = (30, 13)

    def items(self):
        height, _ = self.item_size
        with open(self.data_filepath, 'r') as data_file:
            with open(self.labels_filepath, 'r') as labels_file:
                items = []
                spectogram = []
                for index, line in enumerate(data_file):
                    spectogram.append(list(line.replace('\n', '')))
                    if index % height == height - 1:
                        label = int(labels_file.readline().replace('\n', ''))
                        yield (spectogram, label)
                        spectogram = []

                        data_file.readline()
                        data_file.readline()
                        data_file.readline()

if __name__ == '__main__':
    height = 30
    width = 13
    parser = Parser('part2data/training_data.txt', 'part2data/training_labels.txt')

    count = 0
    for item in parser.items():
        count += 1

        assert type(item) == tuple

        # check first item in the tuple is our matrix (list of lists)
        assert type(item[ 0 ]) == list

        # check label is an int
        assert type(item[ 1 ]) == int

        # check number of rows is right
        assert len(item[ 0 ]) == height

        # check number of columns is right
        assert len(item[ 0 ][ 0 ]) == width

    assert count == 60
