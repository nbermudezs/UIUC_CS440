__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import numpy as np

class SinglePixelFeatureExtractor:
    def items(self, dataset):
        result = []
        for (matrix, label) in dataset:
            flatten = self.extract_from_item(matrix)
            result.append((np.array(flatten), label, matrix))
        return result

    def extract_from_item(self, item):
        return [(0 if item == ' ' else 1) for row in item for item in row]

if __name__ == '__main__':
    import pdb

    item_1 = [
        [ ' ', '+', ' ', ' ' ],
        [ ' ', '+', '#', ' ' ],
        [ ' ', '+', '#', ' ' ],
        [ ' ', '+', '#', ' ' ]
    ]
    item_2 = [
        [ ' ', '+', ' ', ' ' ],
        [ ' ', '+', '#', ' ' ],
        [ ' ', '+', '#', ' ' ],
        [ ' ', '+', '#', ' ' ]
    ]
    dataset = [ (item_1, 1), (item_2, 2) ]
    extractor = SinglePixelFeatureExtractor()

    first = next(extractor.items(dataset))
    pdb.set_trace()
