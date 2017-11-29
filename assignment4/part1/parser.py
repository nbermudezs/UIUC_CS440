__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from util import Util

import pdb

class Parser:
    def __init__(self, data_filepath, labels_filepath, item_size):
        self.data_filepath = data_filepath
        self.labels_filepath = labels_filepath
        self.item_size = item_size

    def items(self):
        size_range = range(self.item_size)
        with open(self.data_filepath, 'r') as data_file:
            with open(self.labels_filepath) as labels_file:
                items = []
                digit_matrix = []
                for index, line in enumerate(data_file):
                    digit_matrix.append(list(line.replace('\n', '')))
                    if index % self.item_size == self.item_size - 1:
                        label = int(labels_file.readline().replace('\n', ''))
                        yield (digit_matrix, label)
                        digit_matrix = []

if __name__ == '__main__':
    size = 28
    parser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', size)
    for item in parser.items():
        assert type(item) == tuple

        # check first item in the tuple is our matrix (list of lists)
        assert type(item[ 0 ]) == list

        # check label is an int
        assert type(item[ 1 ]) == int

        # check number of rows is right
        assert len(item[ 0 ]) == size

        # check number of columns is right
        assert len(item[ 0 ][ 0 ]) == size
