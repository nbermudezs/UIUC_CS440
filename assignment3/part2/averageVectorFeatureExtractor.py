from __future__ import division

__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from collections import defaultdict
import pdb

BLANK = ' '

class AverageVectorFeatureExtractor:
    def items(self, dataset):
        for (matrix, label) in dataset:
            features = self.extract_from_item(matrix)
            yield (features, label, matrix)

    def extract_from_item(self, item):
        cols = len(item[ 0 ])
        counts = defaultdict(lambda: 0)

        for row in item:
            for col in range(cols):
                if row[ col ] == BLANK:
                    counts[ col ] += 1
        return [ counts[ col ] / cols for col in range(cols) ]

if __name__ == '__main__':
    import pdb

    item_1 = [
        [ ' ', '%', ' ', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', '%' ]
    ]
    item_2 = [
        [ ' ', '%', ' ', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ]
    ]
    dataset = [ (item_1, 'y'), (item_2, 2) ]
    extractor = AverageVectorFeatureExtractor()

    features, label, original = next(extractor.items(dataset))

    assert label == 'y'
    assert features[ 0 ] == 1
    assert features[ 1 ] == 0
    assert features[ 2 ] == 0.25
    assert features[ 3 ] == 0.75
    assert original == item_1
