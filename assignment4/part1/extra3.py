__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from differentiableClassifier import DigitClassifier
from learningRate import LearningRate
from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from parser import Parser
from util import Util

from scipy.special import expit
import numpy as np

def sigmoid_descent(w, x):
    return expit(np.dot(w, x)) * (1 - expit(np.dot(w, x)))

if __name__ == '__main__':
    import pdb
    from time import time

    start = time()
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(
        descent=sigmoid_descent,
        epochs=1000,
        learning_rate=1000,
        learning_rate_decay=lambda x,y: 0.1,
        shuffle=True,
        use_bias=True,
        zero_weights=True)
    training_curve = classifier.train(extractor.items(digitParser.items()))
    print('Training time: ', time() - start)
    Util.plot_training_curve(training_curve)

    start = time()
    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Overall accuracy: ', round(acc * 100, 2))
    print('Test time: ', time() - start)
