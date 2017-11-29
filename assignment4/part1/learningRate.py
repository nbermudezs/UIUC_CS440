__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import numpy as np

'''
    Ideas of the different decay functions that are
    usually applied were taken from TensorFlow's documentation.
    See: https://www.tensorflow.org/versions/r0.12/api_docs/python/train/decaying_the_learning_rate
'''
class LearningRate:
    def inverse_time_decay(learning_rate, t):
        return learning_rate / (learning_rate + t)

    def exponential_decay(learning_rate, t, mu=0.1):
        return np.exp(-mu * t)
