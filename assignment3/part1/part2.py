__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from pixelGroupFeatureExtractor import PixelGroupFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import pdb
    import time

    group_height = 4
    group_width = 4
    disjoint = False

    training_time = -time.clock()
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = PixelGroupFeatureExtractor(group_width, group_height, disjoint)
    classifier = DigitClassifier(smoothing = 0.001)
    classifier.train(extractor.items(digitParser.items()))
    training_time += time.clock()

    evaluation_time = -time.clock()
    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, count, feature_count = classifier.evaluate(extractor.items(evaluationData.items()))
    evaluation_time += time.clock()
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Group size: ' + str(group_width) + 'x' + str(group_height))
    print('Disjoint groups?', disjoint)
    print('Number of features: ', feature_count)
    print('Overall accuracy: ', round(acc * 100, 2))
    print('Training time: ', training_time)
    print('Overall evaluation time: ', evaluation_time)
    print('Per example evaluation time: ', evaluation_time / count)

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
