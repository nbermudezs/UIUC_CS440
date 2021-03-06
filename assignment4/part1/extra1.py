__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from classifier import DigitClassifier
from learningRate import LearningRate
from pixelGroupFeatureExtractor import PixelGroupFeatureExtractor
from parser import Parser
from util import Util

if __name__ == '__main__':
    import numpy as np
    import pdb
    import time

    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = PixelGroupFeatureExtractor(3, 2)
    classifier = DigitClassifier(
        epochs=100,
        learning_rate=1000,
        learning_rate_decay=LearningRate.inverse_time_decay,
        shuffle=True,
        use_bias=True,
        zero_weights=True)
    training_curve = classifier.train(extractor.items(digitParser.items()))
    Util.plot_training_curve(training_curve)

    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Overall accuracy: ', round(acc * 100, 2))
