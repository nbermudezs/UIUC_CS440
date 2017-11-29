__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from knnClassifier import DigitClassifier
from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from parser import Parser
from util import Util

from scipy.spatial.distance import cosine, euclidean, jaccard

import numpy as np

if __name__ == '__main__':
    import numpy as np
    import pdb
    import sys
    from time import time

    if len(sys.argv) > 1:
        k = int(sys.argv[1])
    else:
        k = 1

    start = time()
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    classifier = DigitClassifier(k=k, distance=euclidean)
    classifier.train(extractor.items(digitParser.items()))
    print('Training time: ', time() - start)

    start = time()
    evaluationData = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    confusion_matrix, acc, _, _ = classifier.evaluate(extractor.items(evaluationData.items()))
    Util.print_confusion_matrix(confusion_matrix, 10, 10)
    print('Overall accuracy: ', round(acc * 100, 2))
    print('Testing time: ', time() - start)
