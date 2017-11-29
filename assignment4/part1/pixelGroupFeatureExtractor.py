__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

EMPTY = ' '

class PixelGroupFeatureExtractor:
    def __init__(self, group_rows = 2, group_cols = 2, disjoint = False):
        self.group_rows = group_rows
        self.group_cols = group_cols
        self.disjoint = disjoint

    def items(self, dataset):
        result = []
        for (matrix, label) in dataset:
            features = self.extract_from_item(matrix)
            result.append((features, label, matrix))
        return result

    def extract_from_item(self, item):
        features = []
        size_rows = len(item)
        size_cols = len(item[ 0 ])
        row = 0
        while row < size_rows:
            col = 0
            if row + self.group_rows > size_rows:
                break
            while col < size_cols:
                if col + self.group_cols > size_cols:
                    break
                feature = ''
                for delta_r in range(self.group_rows):
                    for delta_c in range(self.group_cols):
                        feature += self.get_value(item, row + delta_r, col + delta_c)
                features.append(int(feature))
                col += self.group_cols if self.disjoint else 1
            row += self.group_rows if self.disjoint else 1
        return features

    def get_value(self, matrix, row, col):
        return '0' if matrix[ row ][ col ] == EMPTY else '1'
