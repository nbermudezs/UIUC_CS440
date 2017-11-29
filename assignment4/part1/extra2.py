__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from heatMap import HeatMap
from learningRate import LearningRate
from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import numpy as np
    import pdb
    import time

    use_bias = True
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(
        epochs=100,
        learning_rate=1000,
        learning_rate_decay=LearningRate.inverse_time_decay,
        shuffle=True,
        use_bias=use_bias,
        zero_weights=True)
    classifier.train(extractor.items(digitParser.items()))

    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))

    for label in list(confusion_matrix.keys()):
        if use_bias:
            weights = classifier.weights[label][1:].reshape(28, 28)
        else:
            weights = classifier.weights[label].reshape(28, 28)
        HeatMap.display(weights, 'Color map for class ' + str(label))
