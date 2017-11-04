__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from heatMap import HeatMap
from parser import Parser
from util import Util

if __name__ == '__main__':
    import pdb

    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(smoothing = 5)
    classifier.train(extractor.items(digitParser.items()))

    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Overall accuracy: ', round(acc * 100, 2))

    labels = sorted(list(classifier.highest_likely_examples.keys()))
    for label in labels:
        features,_ = classifier.highest_likely_examples[ label ]
        print('Highest likelihood for class: ', label)
        Util.print_matrix(features, 28, 28)
        print('\n')

        features,_ = classifier.lowest_likely_examples[ label ]
        print('Lowest likelihood for class: ', label)
        Util.print_matrix(features, 28, 28)
        print('\n\n')

    for_inspection = Util.pick_pairs_for_inspection(confusion_matrix)
    for ref_label, label in for_inspection:
        likelihood = classifier.model_likelihood(ref_label)
        HeatMap.display(likelihood, 'Log likelihood for class ' + str(ref_label))

        likelihood = classifier.model_likelihood(label)
        HeatMap.display(likelihood, 'Log likelihood for class ' + str(label))

        ratios = classifier.model_odd_ratios(ref_label, label)
        HeatMap.display(ratios, 'Log odd ratios between classes ' + str(ref_label) + ' and ' + str(label))
