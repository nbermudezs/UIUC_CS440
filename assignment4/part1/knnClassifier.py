__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import numpy as np
from queue import PriorityQueue
from collections import defaultdict

class kNNClassifier:
    def __init__(self, k=5, distance=None):
        self.k = k
        self.distance = distance

    def train(self, data):
        self.neighbors = data

    def evaluate(self, data):
        correctly_predicted_count = 0
        example_count = 0
        confusion_matrix = {}

        for features, label, _ in data:
            distances = PriorityQueue()
            for neighbor, predicted_label, _ in self.neighbors:
                dist = self.distance(neighbor, features)
                distances.put((dist, predicted_label))

            counts = defaultdict(lambda: 0)
            for _ in range(self.k):
                _, label = distances.get()
                counts[label] += 1
            predicted_label = max(counts.keys(), key=lambda label: counts[label])

            feature_count = len(features)
            example_count += 1
            if predicted_label == label:
                correctly_predicted_count += 1
            self._add_to_confusion_matrix(confusion_matrix, label, predicted_label)
        return (confusion_matrix, correctly_predicted_count / example_count, example_count, feature_count)

    def _add_to_confusion_matrix(self, matrix, expected, predicted):
        row = matrix.get(expected, {})
        count = row.get(predicted, 0)
        row[ predicted ] = count + 1
        matrix[ expected ] = row


DigitClassifier = kNNClassifier
