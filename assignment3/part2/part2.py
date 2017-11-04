__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import NaiveBayesClassifier
from singleBlockFeatureExtractor import SingleBlockFeatureExtractor
from digitsAudioParser import DigitsAudioParser
from util import Util

if __name__ == '__main__':
    import pdb

    parser = DigitsAudioParser('part2data/training_data.txt', 'part2data/training_labels.txt')
    extractor = SingleBlockFeatureExtractor()
    classifier = NaiveBayesClassifier(smoothing = 5)
    classifier.train(extractor.items(parser.items()))

    evaluationData = DigitsAudioParser('part2data/testing_data.txt', 'part2data/testing_labels.txt')
    confusion_matrix, acc = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 5, 5)
    print('Overall accuracy: ', round(acc * 100, 2))

    labels = sorted(list(classifier.highest_likely_examples.keys()))
    for label in labels:
        features,_ = classifier.highest_likely_examples[ label ]
        print('Highest likelihood for class: ', label)
        Util.print_matrix(features, 30, 13)
        print('\n')

        features,_ = classifier.lowest_likely_examples[ label ]
        print('Lowest likelihood for class: ', label)
        Util.print_matrix(features, 30, 13)
        print('------------------------------')
        print('\n\n')

    pdb.set_trace()
