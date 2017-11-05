__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from heatMap import HeatMap
from parser import Parser
from util import Util

"""
Returns tuple of accuracy, training_time, evaluation_time, # of eval examples
"""
def train(smoothing):
    training_time = -time.clock()
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(smoothing = smoothing)
    classifier.train(extractor.items(digitParser.items()))
    training_time += time.clock()

    evaluation_time = -time.clock()
    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, count, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    evaluation_time += time.clock()
    return acc * 100, training_time, evaluation_time, count

if __name__ == '__main__':
    import numpy as np
    import pdb
    import time

    min_smoothing = 0.2
    max_smoothing = 10.0
    best_smoothing = None
    best_accuracy = -float('inf')
    trial_count = 0
    total_training_time = 0
    total_evaluation_time = 0
    total_evaluation_examples = 0
    for smoothing in np.arange(min_smoothing, max_smoothing, 0.2):
        trial_count += 1
        start = time.clock()
        accuracy, train_time, eval_time, count = train(smoothing)
        total_training_time += train_time
        total_evaluation_time += eval_time
        total_evaluation_examples += count

        print('Smoothing =', smoothing, 'achieved', accuracy, 'accuracy')
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_smoothing = smoothing

    print('Best smoothing value: ', best_smoothing)
    print('Accuracy: ', best_accuracy)
    print('Average training time: ', total_training_time / trial_count)
    print('Average evaluation time: ', total_evaluation_time / trial_count)
    print('Average per example classification time: ', total_evaluation_time / total_evaluation_examples)

    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(smoothing = best_smoothing)
    classifier.train(extractor.items(digitParser.items()))

    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
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

    for_inspection = Util.pick_pairs_for_inspection(confusion_matrix)
    for ref_label, label in for_inspection:
        likelihood = classifier.model_likelihood(ref_label)
        HeatMap.display(likelihood, 'Log likelihood for class ' + str(ref_label))

        likelihood = classifier.model_likelihood(label)
        HeatMap.display(likelihood, 'Log likelihood for class ' + str(label))

        ratios = classifier.model_odd_ratios(ref_label, label)
        HeatMap.display(ratios, 'Log odd ratios between classes ' + str(ref_label) + ' and ' + str(label))
