__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from probabilityDistribution import ProbabilityDistribution
import math
import numpy as np
import pdb

inf = float('inf')
LABEL_YES = 1
LABEL_NO = 0

class FisherLDAClassifier:
    def train(self, data):
        class_yes = []
        class_no = []

        for item in data:
            feature_count = len(item[ 0 ])
            if item[ 1 ] == LABEL_YES:
                class_yes.append(item[ 0 ])
            else:
                class_no.append(item[ 0 ])
        class_yes = np.asarray(class_yes, dtype = np.float32)
        class_no = np.asarray(class_no, dtype = np.float32)
        mean_yes = self._class_mean(class_yes)
        mean_no = self._class_mean(class_no)
        within = self._find_within_class_scatter(class_yes, class_no, mean_yes, mean_no)
        self.W = np.dot(np.linalg.pinv(within), (mean_yes - mean_no))
        self.W_0 = (np.dot(self.W, mean_yes) + np.dot(self.W, mean_no)) / 2

    def evaluate(self, data):
        correctly_predicted_count = 0
        example_count = 0
        confusion_matrix = {}
        for (features, label, original) in data:
            example_count += 1
            predicted_label = self.predict(features)
            if predicted_label == label:
                correctly_predicted_count += 1
            self.add_to_confusion_matrix(confusion_matrix, label, predicted_label)
        return (confusion_matrix, correctly_predicted_count / example_count)

    def predict(self, example_features):
        if np.dot(self.W.T, example_features) >= self.W_0:
            return LABEL_YES
        else:
            return LABEL_NO

    def _class_mean(self, class_data):
        return np.mean(class_data, axis = 0).T

    def _find_within_class_scatter(self, class_yes, class_no, mean_yes, mean_no):
        diff_yes = self._mean_difference(class_yes, mean_yes)
        diff_no = self._mean_difference(class_no, mean_no)
        all_diff = np.concatenate((diff_no, diff_yes))

        rows, cols = all_diff.shape
        all_diff = np.matrix(all_diff)

        within = np.zeros((cols, cols))
        for row in all_diff:
            within += np.dot(row.T, row)

        return within

    def _mean_difference(self, data, mean):
        rows, cols = data.shape
        return data - np.array(list(mean) * rows).reshape(rows, cols)

    def add_to_confusion_matrix(self, matrix, expected, predicted):
        row = matrix.get(expected, {})
        count = row.get(predicted, 0)
        row[ predicted ] = count + 1
        matrix[ expected ] = row

if __name__ == '__main__':
    class_1 = [ (1, 2), (2, 3), (3, 3), (4, 5), (5, 5) ]
    class_2 = [ (1,0), (2,1), (3,1), (3,2), (5,3), (6,5) ]
    dataset = []
    for x in class_1:
        dataset.append((list(x), 0, None))
    for x in class_2:
        dataset.append((list(x), 1, None))

    classifier = FisherLDAClassifier()
    classifier.train(dataset)
