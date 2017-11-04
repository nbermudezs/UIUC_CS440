__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

BLANK = ' '

class SingleBlockFeatureExtractor:
    def items(self, dataset):
        for (matrix, label) in dataset:
            flatten = self.extract_from_item(matrix)
            yield (flatten, label, matrix)

    def extract_from_item(self, item):
        return [(1 if item == BLANK else 0) for row in item for item in row]

if __name__ == '__main__':
    import pdb

    item_1 = [
        [ ' ', '%', ' ', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ]
    ]
    item_2 = [
        [ ' ', '%', ' ', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ],
        [ ' ', '%', '%', ' ' ]
    ]
    dataset = [ (item_1, 'y'), (item_2, 2) ]
    extractor = SingleBlockFeatureExtractor()

    features, label, original = next(extractor.items(dataset))

    assert label == 'y'
    assert features[ 0 ] == 1
    assert features[ 1 ] == 0
    assert original == item_1
