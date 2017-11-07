__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from fisherLDAClassifier import FisherLDAClassifier
from singleBlockFeatureExtractor import SingleBlockFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import pdb
    import time

    start = time.clock()
    parser = Parser('part1data/yes_train.txt', 'part1data/no_train.txt')
    extractor = SingleBlockFeatureExtractor(lambda x: 1 if x == 'y' else 0)
    classifier = FisherLDAClassifier()
    classifier.train(extractor.items(parser.items()))
    print('Training time: ' + str((time.clock() - start) * 1000) + 'ms')

    evaluationData = Parser('part1data/yes_test.txt', 'part1data/no_test.txt')
    confusion_matrix, acc = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 2, 2)
    print('Overall accuracy: ', round(acc * 100, 2))
