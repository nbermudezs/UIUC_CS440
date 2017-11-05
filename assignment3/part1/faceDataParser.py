__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from util import Util

import pdb

class FaceDataParser:
    def __init__(self, data_filepath, labels_filepath):
        self.data_filepath = data_filepath
        self.labels_filepath = labels_filepath
        self.item_size = (70, 60)

    def items(self):
        height,_ = self.item_size
        with open(self.data_filepath, 'r') as data_file:
            with open(self.labels_filepath) as labels_file:
                items = []
                face_matrix = []
                for index, line in enumerate(data_file):
                    face_matrix.append(list(line.replace('\n', '')))
                    if index % height == height - 1:
                        label = int(labels_file.readline().replace('\n', ''))
                        yield (face_matrix, 'non-face' if label == 0 else 'face')
                        face_matrix = []

if __name__ == '__main__':
    height, width = 70, 60
    parser = FaceDataParser('extradata/facedatatrain', 'extradata/facedatatrainlabels')
    for item in parser.items():
        assert type(item) == tuple

        # check first item in the tuple is our matrix (list of lists)
        assert type(item[ 0 ]) == list

        # check label is an int
        assert type(item[ 1 ]) == str
        assert item[ 1 ] == 'face' or item[ 1 ] == 'non-face'

        # check number of rows is right
        assert len(item[ 0 ]) == height

        # check number of columns is right
        assert len(item[ 0 ][ 0 ]) == width
