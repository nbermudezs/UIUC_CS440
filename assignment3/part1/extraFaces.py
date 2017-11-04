__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import NaiveBayesClassifier
from pixelGroupFeatureExtractor import PixelGroupFeatureExtractor
from faceDataParser import FaceDataParser
from util import Util

if __name__ == '__main__':
    import pdb

    parser = FaceDataParser('extradata/facedatatrain', 'extradata/facedatatrainlabels')
    extractor = PixelGroupFeatureExtractor(2, 2)
    classifier = NaiveBayesClassifier(smoothing = 5)
    classifier.train(extractor.items(parser.items()))

    evaluationData = FaceDataParser('extradata/facedatatest', 'extradata/facedatatestlabels')
    confusion_matrix, acc = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 2, 2, show_legends = True)
    print('Overall accuracy: ', round(acc * 100, 2))

    labels = sorted(list(classifier.highest_likely_examples.keys()))
    for label in labels:
        features,_ = classifier.highest_likely_examples[ label ]
        print('Highest likelihood for class: ', label)
        Util.print_as_string(features, parser.item_size[ 0 ], parser.item_size[ 1 ])
        print('\n')

        features,_ = classifier.lowest_likely_examples[ label ]
        print('Lowest likelihood for class: ', label)
        Util.print_as_string(features, parser.item_size[ 0 ], parser.item_size[ 1 ])
        print('\n\n')
