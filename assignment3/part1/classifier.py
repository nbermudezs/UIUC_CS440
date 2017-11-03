__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from probabilityDistribution import ProbabilityDistribution

import math
import pdb

inf = float('inf')

class DigitClassifier:
    def __init__(self, smoothing = 1, size = 28):
        self.distributions = {}
        self.class_frequencies = {}
        self.total_count = 0
        self.smoothing = smoothing
        self.size = size
        self.highest_likely_examples = {}
        self.lowest_likely_examples = {}

    def train(self, data):
        distributions = self.distributions
        class_frequencies = self.class_frequencies

        for (features, label, _) in data:
            self.total_count += 1

            count = class_frequencies.get(label, 0)
            count += 1
            class_frequencies[ label ] = count

            class_dist = distributions.get(label, {})
            for index, feature in enumerate(features):
                feature_dist = class_dist.get(index, ProbabilityDistribution(self.smoothing))
                feature_dist.add(feature)
                class_dist[ index ] = feature_dist
            distributions[ label ] = class_dist

    def prior(self, label):
        return self.class_frequencies[ label ] / self.total_count

    """
    Returns a list of tuples. Each tuple represents the likelihood of the item
    being classified as a given class.
    Class is the first item in the tuple, likelihood second.
    """
    def MAP(self, features):
        classes = list(self.class_frequencies.keys())

        result = []
        for _class in classes:
            dist = self.distributions[ _class ]
            likelihood = self._log_likelihood(_class, dist, features)
            result.append((_class, likelihood))
        return result

    def _log_likelihood(self, _class, class_dist, features):
        likelihood = math.log(self.prior(_class))
        for (index, feature) in enumerate(features):
            dist = class_dist[ index ]
            likelihood += dist.log_p_of(feature)
        return likelihood

    def predict(self, features):
        maps = self.MAP(features)
        return max(maps, key=lambda x:x[ 1 ])

    def evaluate(self, data):
        confusion_matrix = {}
        for (features, label, original) in data:
            predicted_label, likelihood = self.predict(features)
            self.add_to_confusion_matrix(confusion_matrix, label, predicted_label)

            highest = self.highest_likely_examples.get(predicted_label, (None, -inf))
            if likelihood > highest[ 1 ]:
                self.highest_likely_examples[ predicted_label ] =\
                    (original, likelihood)

            lowest = self.lowest_likely_examples.get(predicted_label, (None, inf))
            if likelihood < lowest[ 1 ]:
                self.lowest_likely_examples[ predicted_label ] =\
                    (original, likelihood)
        return confusion_matrix

    def add_to_confusion_matrix(self, matrix, expected, predicted):
        row = matrix.get(expected, {})
        count = row.get(predicted, 0)
        row[ predicted ] = count + 1
        matrix[ expected ] = row

    def features_likelihood(self, features, label):
        class_dist = self.distributions[ label ]
        matrix = []
        for (idx, feature) in enumerate(features):
            row = idx // self.size
            if len(matrix) <= row:
                matrix = [[]] + matrix
            row = matrix[ 0 ]
            dist = class_dist[ idx ]
            value = dist.log_p_of(feature)
            row.append(value)
        return matrix
