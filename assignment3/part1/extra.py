__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from ternaryFeatureExtractor import TernaryFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import pdb

    smoothing = 0.001
    group_width = 2
    group_height = 2
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = TernaryFeatureExtractor(group_height, group_width)
    classifier = DigitClassifier(smoothing = smoothing)
    classifier.train(extractor.items(digitParser.items()))

    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Smoothing constant: ', smoothing)
    print('Group size: ', group_width, 'x', group_height)
    print('Overall accuracy: ', round(acc * 100, 2))

    labels = sorted(list(classifier.highest_likely_examples.keys()))
    for label in labels:
        features,_ = classifier.highest_likely_examples[ label ]
        print('Highest likelihood for class: ', label)
        Util.print_as_string(features, 28, 28)
        print('\n')

        features,_ = classifier.lowest_likely_examples[ label ]
        print('Lowest likelihood for class: ', label)
        Util.print_as_string(features, 28, 28)
        print('\n\n')
