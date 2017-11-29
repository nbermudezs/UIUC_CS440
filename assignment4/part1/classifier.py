__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import numpy as np
import random

INF = float('inf')

class PerceptronClassifier:
    def __init__(self,
                 learning_rate=None,
                 epochs=100,
                 use_bias=True,
                 zero_weights=True,
                 shuffle=True,
                 n_classes=10):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.use_bias = use_bias
        self.zero_weights = zero_weights
        self.shuffle = shuffle
        self.n_classes = n_classes

    '''
        self.weights is an array of size self.n_classes
        each element in the array is itself an array containing the weights
        for the i-th classifier.
    '''
    def train(self, data):
        training_curve = []
        self.weights = weights = self._init_weights(data)

        for epoch in range(self.epochs):
            alpha = self.learning_rate(epoch)

            indices = list(range(len(data)))
            if self.shuffle:
                random.shuffle(indices)

            for idx in indices:
                features, label, _ = data[idx]
                if self.use_bias:
                    features = np.concatenate([[1], features])

                predicted_label = None
                best_prediction = -INF
                for i, class_weights in enumerate(weights):
                    prediction = np.dot(np.transpose(class_weights), features)
                    if prediction > best_prediction:
                        best_prediction = prediction
                        predicted_label = i

                # update weights if misclassified
                if predicted_label != label:
                    w_c = weights[label]
                    w_c_prime = weights[predicted_label]
                    weights[label] = w_c + alpha * features
                    weights[predicted_label] = w_c_prime - alpha * features

            _, accuracy, _, _ = self.evaluate(data)
            training_curve.append(accuracy)

        return training_curve

    def evaluate(self, data):
        correctly_predicted_count = 0
        example_count = 0
        confusion_matrix = {}
        for features, label, _ in data:
            if self.use_bias:
                features = np.concatenate([[1], features])
            best_prediction = -INF
            predicted_label = None
            for idx in range(self.n_classes):
                weights = self.weights[idx]
                prediction = np.dot(weights, features)
                if prediction > best_prediction:
                    best_prediction = prediction
                    predicted_label = idx
            feature_count = len(features)
            example_count += 1
            if predicted_label == label:
                correctly_predicted_count += 1
            self._add_to_confusion_matrix(confusion_matrix, label, predicted_label)
        return (confusion_matrix, correctly_predicted_count / example_count, example_count, feature_count)

    def _init_weights(self, data):
        dimensionality = len(data[0][0]) # # of features in first example
        if self.use_bias:
            dimensionality += 1

        all_weights = []
        for _ in range(self.n_classes):
            if self.zero_weights:
                weights = np.zeros(dimensionality)
            else:
                weights = np.array([random.random() for _ in range(dimensionality)])
            all_weights.append(weights)
        return all_weights

    def _add_to_confusion_matrix(self, matrix, expected, predicted):
        row = matrix.get(expected, {})
        count = row.get(predicted, 0)
        row[ predicted ] = count + 1
        matrix[ expected ] = row

DigitClassifier = PerceptronClassifier
