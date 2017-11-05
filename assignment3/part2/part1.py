__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import NaiveBayesClassifier
from singleBlockFeatureExtractor import SingleBlockFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import pdb

    parser = Parser('part1data/yes_train.txt', 'part1data/no_train.txt')
    extractor = SingleBlockFeatureExtractor()
    classifier = NaiveBayesClassifier(smoothing = 5)
    classifier.train(extractor.items(parser.items()))

    evaluationData = Parser('part1data/yes_test.txt', 'part1data/no_test.txt')
    confusion_matrix, acc = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 2, 2)
    print('Overall accuracy: ', round(acc * 100, 2))

    labels = sorted(list(classifier.highest_likely_examples.keys()))
    for label in labels:
        features,_ = classifier.highest_likely_examples[ label ]
        print('Highest likelihood for class: ', label)
        Util.print_as_string(features, 25, 10)
        print('\n')

        features,_ = classifier.lowest_likely_examples[ label ]
        print('Lowest likelihood for class: ', label)
        Util.print_as_string(features, 25, 10)
        print('------------------------------')
        print('\n\n')
