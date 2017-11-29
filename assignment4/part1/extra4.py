__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from singlePixelFeatureExtractor import SinglePixelFeatureExtractor
from parser import Parser
from sklearn.svm import SVC

def process_data(data):
    X_train = []
    y_train = []
    for features, label, _ in data:
        X_train.append(features)
        y_train.append(label)
    return X_train, y_train

if __name__ == '__main__':
    import numpy as np
    import pdb
    from time import time

    '''
        Ref: http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    '''
    print('Classifying using SVC from sklearn.')
    start = time()
    digitParser = Parser('digitdata/trainingimages', 'digitdata/traininglabels', 28)
    extractor = SinglePixelFeatureExtractor()
    X_train, y_train = process_data(extractor.items(digitParser.items()))
    classifier = SVC(kernel='linear')
    classifier.fit(X_train, y_train)
    print('Training time: ', time() - start)

    start = time()
    digitParser = Parser('digitdata/testimages', 'digitdata/testlabels', 28)
    X_test, y_test = process_data(extractor.items(digitParser.items()))
    accuracy = classifier.score(X_test, y_test)
    print('Overall accuracy: ', round(accuracy *  100, 2))
    print('Testing time: ', time() - start)
