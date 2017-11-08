__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import numpy as np
import os
import pdb

LABEL_YES = 'y'
LABEL_NO = 'n'
LOW_ENERGY = '%'
ENTRIES_PER_FILE = 8
ENTRY_WIDTH = 10

class UnsegmentedDataParser:
    def __init__(self, directory):
        self.directory = directory

    def items(self):
        files = os.listdir(self.directory)
        for file_name in files:
            labels = [ LABEL_YES if item == '1' else LABEL_NO
                       for item in file_name.replace('.txt', '').split('_') ]
            input_data = self._split_file_data(file_name)
            for i, features in enumerate(input_data):
                yield (features.tolist(), labels[ i ])
        # pdb.set_trace()

    def _split_file_data(self, file_name):
        result = []
        with open(self.directory + '/' + file_name, 'r') as data_file:
            matrix = [ list(line.replace('\n', '')) for line in data_file ]
            matrix = np.matrix(matrix)
            transpose = matrix.T
            data_start = self._find_data_start(transpose)
            for i in range(ENTRIES_PER_FILE):
                data = transpose[i * ENTRY_WIDTH + data_start:(i + 1) * ENTRY_WIDTH + data_start]
                result.append(data.T)
            return result

    def _find_data_start(self, matrix):
        for i, row in enumerate(matrix):
            if i == len(matrix) - 1:
                continue

            row_low = self._get_row_low_percentage(np.array(row))
            next_row_low = self._get_row_low_percentage(np.array(matrix[ i + 1 ]))
            if row_low < (23/25) and next_row_low < row_low:
                return i
        return 0


    def _get_row_low_percentage(self, row):
        unique, counts = np.unique(row, return_counts = True)
        aggregation = dict(zip(unique, counts))
        return aggregation[ LOW_ENERGY ] / len(row[ 0 ])


if __name__ == '__main__':
    parser = UnsegmentedDataParser('extradata')
    result = parser.items()
    next(result)
